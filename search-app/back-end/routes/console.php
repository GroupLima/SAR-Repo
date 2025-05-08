<?php

use Illuminate\Foundation\Inspiring;
use Illuminate\Support\Facades\Artisan;
use App\Http\Controllers\RecordController;
use Illuminate\Support\Facades\Schedule;
use Illuminate\Support\Facades\Cache;
 
Schedule::command('preload:records')->withoutOverlapping()->runInBackground();

Artisan::command('inspire', function () {
    $this->comment(Inspiring::quote());
})->purpose('Display an inspiring quote')->hourly();

Artisan::command('preload:records', function () {
    $lock = Cache::lock('preload-lock', 60);

    if ($lock->get()) {
        try {
            $controller = new RecordController();
            $volumes = ['1', '2', '4', '5', '6', '7', '8'];

            foreach ($volumes as $volume) {
                $results = $controller->loadRecords($volume);
                if ($results) {
                    Cache::put("preload_volume_{$volume}", $results);
                } else {
                    $this->error("Failed to preload volume {$volume}.");
                }
            }

            $this->info('Records preloaded into cache.');
        } finally {
            $lock->release();
        }
    } else {
        $this->info('Preload already in progress or recently completed.');
    }
})->purpose('Preload records on server start');