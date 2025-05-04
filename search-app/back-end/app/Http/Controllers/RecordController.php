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
            storage_path('xml-files/XML files volumes 1-7'),
            storage_path('xml-files/XML files volume 8'),
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

                $namespaces = $xml->getNamespaces(true);
                $teiBody = $xml->children($namespaces[''])->text->body;

                foreach ($teiBody->div as $div) {
                    foreach ($div->{'div'} as $entry) {
                        $type = (string) $entry['type'];
                        $id = (string) $entry['xml:id'];
                        $lang = (string) $entry['xml:lang'];

                        if ($type === 'entry' && str_contains($id, 'ARO-' . $volume . '-')) {
                            // Attempt to extract date from parent <div> if present
                            $date = '';
                            if (isset($div->p->date['when'])) {
                                $date = (string) $div->p->date['when'];
                            }

                            $records[] = [
                                'id' => $id,
                                'language' => $lang,
                                'content' => strip_tags($entry->asXML()),
                                'date' => $date,
                            ];
                        }
                    }
                }
            }
        }

        // Pagination
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
            storage_path('xml-files/XML files volumes 1-7'),
            storage_path('xml-files/XML files volume 8'),
        ];

        foreach ($directories as $dir) {
            if (!is_dir($dir)) continue;

            foreach (scandir($dir) as $file) {
                if (!str_ends_with($file, '.xml')) continue;

                $filePath = $dir . DIRECTORY_SEPARATOR . $file;

                libxml_use_internal_errors(true);
                $xml = simplexml_load_file($filePath);
                if (!$xml) continue;

                $namespaces = $xml->getNamespaces(true);
                $body = $xml->children($namespaces[''])->text->body;

                foreach ($body->div as $outerDiv) {
                    foreach ($outerDiv->{'div'} as $entry) {
                        $entryId = (string) $entry['xml:id'];
                        if ($entryId === $id) {
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
            }
        }

        return response()->json(['error' => 'XML entry not found'], 404);
    }
}
