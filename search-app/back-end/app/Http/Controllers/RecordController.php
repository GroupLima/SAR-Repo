<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;

class RecordController extends Controller
{
    public function getVolumes()
    {
        // Static for now; can be made dynamic later
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
            if (!is_dir($dir)) continue;

            foreach (scandir($dir) as $file) {
                if (!str_ends_with($file, '.xml')) continue;

                $filePath = $dir . DIRECTORY_SEPARATOR . $file;
                libxml_use_internal_errors(true);
                $xml = simplexml_load_file($filePath);
                if (!$xml) continue;

                $xml->registerXPathNamespace('tei', 'http://www.tei-c.org/ns/1.0');
                $entries = $xml->xpath('//tei:div[@type="entry"]');

                foreach ($entries as $entry) {
                    $id = (string) $entry['xml:id'];

                    if (str_starts_with($id, 'ARO-' . $volume . '-')) {
                        $lang = (string) $entry['xml:lang'];
                        $content = strip_tags($entry->asXML());

                        $date = '';
                        $dateNode = $entry->xpath('preceding::tei:date[1]');
                        if (!empty($dateNode)) {
                            $date = (string) $dateNode[0]['when'];
                        }

                        $records[] = [
                            'id' => $id,
                            'language' => $lang,
                            'content' => $content,
                            'date' => $date,
                        ];
                    }
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
                $entry = $xml->xpath('//tei:div[@xml:id="' . $id . '"]');

                if (!empty($entry)) {
                    $dom = dom_import_simplexml($entry[0]);
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
