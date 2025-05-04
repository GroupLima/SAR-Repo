<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;

class RecordController extends Controller
{
    public function getVolumes()
    {
        return response()->json([
            1 => 20,
            2 => 15,
            4 => 25,
            5 => 18,
            6 => 22,
            7 => 16,
            8 => 19,
        ]);
    }

    public function getRecords(Request $request)
    {
        $volume = $request->query('volume');
        $page = $request->query('page');

        if (!$volume || !$page) {
            return response()->json(['error' => 'Volume and page are required'], 400);
        }

        $directories = [
            storage_path('app/xml-files/XML files volumes 1-7'),
            storage_path('app/xml-files/XML files volume 8'),
        ];

        $records = [];

        foreach ($directories as $dir) {
            if (!is_dir($dir)) {
                \Log::error("Directory not found: $dir");
                continue;
            }

            foreach (scandir($dir) as $file) {
                if (!str_ends_with($file, '.xml')) continue;

                $filePath = $dir . DIRECTORY_SEPARATOR . $file;
                \Log::info("Processing file: $filePath");

                libxml_use_internal_errors(true);
                $xml = simplexml_load_file($filePath);

                if (!$xml) {
                    \Log::error("Failed to parse XML: " . print_r(libxml_get_errors(), true));
                    continue;
                }

                $xml->registerXPathNamespace('tei', 'http://www.tei-c.org/ns/1.0');
                $xml->registerXPathNamespace('xml', 'http://www.w3.org/XML/1998/namespace');

                $entries = $xml->xpath('//tei:div[@type="entry" or @type="incompleteEntry"]');

                foreach ($entries as $entry) {
                    $id = (string)$entry->attributes('xml', true)->id;
                    $lang = (string)$entry->attributes('xml', true)->lang;

                    // Filter for volume
                    if (!str_starts_with($id, 'ARO-' . $volume . '-')) {
                        continue;
                    }

                    // Get date from previous sibling
                    $date = '';
                    $precedingElements = $entry->xpath('preceding-sibling::tei:p[1]/tei:date[@when]');
                    if (!empty($precedingElements)) {
                        $date = (string)$precedingElements[0]['when'];
                    }

                    $content = '';
                    if ($entry->head) {
                        $content .= (string)$entry->head . "\n";
                    }
                    if ($entry->p) {
                        $content .= strip_tags($entry->p->asXML());
                    }

                    $records[] = [
                        'id' => $id,
                        'language' => $lang,
                        'content' => $content,
                        'date' => $date,
                    ];

                    \Log::info("Found entry: $id");
                }
            }
        }

        $perPage = 10;
        $offset = ($page - 1) * $perPage;
        $paginated = array_slice($records, $offset, $perPage);

        return response()->json([
            'records' => $paginated,
            'total' => count($records),
        ]);
    }

    public function getXml($id)
    {
        $directories = [
            storage_path('app/xml-files/XML files volumes 1-7'),
            storage_path('app/xml-files/XML files volume 8'),
        ];

        foreach ($directories as $dir) {
            if (!is_dir($dir)) continue;

            foreach (scandir($dir) as $file) {
                if (!str_ends_with($file, '.xml')) continue;

                $filePath = $dir . DIRECTORY_SEPARATOR . $file;
                libxml_use_internal_errors(true);
                $xml = simplexml_load_file($filePath);
                if (!$xml) continue;

                $xml->registerXPathNamespace('tei', 'http://www.tei-c.org/ns/1.0');
                $xml->registerXPathNamespace('xml', 'http://www.w3.org/XML/1998/namespace');

                $entries = $xml->xpath('//tei:div[@xml:id="' . $id . '"]');
                if (!empty($entries)) {
                    $entry = $entries[0];
                    $dom = dom_import_simplexml($entry);
                    $xmlDoc = new \DOMDocument();
                    $xmlDoc->preserveWhiteSpace = false;
                    $xmlDoc->formatOutput = true;
                    $xmlDoc->appendChild($xmlDoc->importNode($dom, true));

                    libxml_clear_errors();
                    return response($xmlDoc->saveXML(), 200)
                        ->header('Content-Type', 'application/xml');
                }
            }
        }

        return response()->json(['error' => 'XML entry not found'], 404);
    }
}
