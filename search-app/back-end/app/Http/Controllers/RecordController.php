<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;

class RecordController extends Controller
{
    public function getVolumes()
    {
        // You can make this dynamic by reading file counts later
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
                $xml = simplexml_load_file($filePath);

                if (!$xml) continue;

                $namespaces = $xml->getNamespaces(true);
                $teiBody = $xml->children($namespaces[''])->text->body;

                foreach ($teiBody->div as $div) {
                    foreach ($div->{'div'} as $entry) {
                        $type = (string) $entry['type'];
                        $id = (string) $entry['xml:id'];
                        $lang = (string) $entry['xml:lang'];
                        $content = trim((string) $entry->asXML());

                        // Basic filtering: check volume in ID
                        if ($type === 'entry' && str_starts_with($id, 'ARO-' . $volume . '-')) {
                            $records[] = [
                                'id' => $id,
                                'language' => $lang,
                                'content' => strip_tags($entry->asXML()),
                                'date' => '', // Optional: extract <date> if needed
                            ];
                        }
                    }
                }
            }
        }

        // Pagination logic
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
                if (str_starts_with($file, $id) && str_ends_with($file, '.xml')) {
                    $path = $dir . DIRECTORY_SEPARATOR . $file;
                    return response(file_get_contents($path), 200)
                        ->header('Content-Type', 'application/xml');
                }
            }
        }

        return response()->json(['error' => 'XML file not found'], 404);
    }
}
