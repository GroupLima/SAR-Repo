<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;

class RecordController extends Controller
{
    public function getVolumes()
    {
        // Example static data (you can fetch from DB later)
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

        // Example static records (replace with DB query later)
        return response()->json([
            'records' => [
                [
                    'id' => 'ARO-1-0001-01',
                    'date' => '1398-09-30',
                    'language' => 'Latin',
                    'content' => 'H Processus Curiarum Balliuorum Isti Sunt...'
                ],
                [
                    'id' => 'ARO-1-0001-02',
                    'date' => '1398-09-30',
                    'language' => 'Latin',
                    'content' => 'Quo die Willelmus de Camera pater cum...'
                ]
            ]
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
    
            $files = scandir($dir);
    
            foreach ($files as $file) {
                if (str_starts_with($file, $id) && str_ends_with($file, '.xml')) {
                    $fullPath = $dir . DIRECTORY_SEPARATOR . $file;
                    $content = file_get_contents($fullPath);
    
                    return response($content, 200)
                        ->header('Content-Type', 'application/xml');
                }
            }
        }
    
        return response()->json(['error' => 'XML file not found'], 404);
    }
    
}