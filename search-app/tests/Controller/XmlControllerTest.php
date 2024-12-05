<?php

namespace Tests\Controllers;

use Tests\TestCase;

class XmlControllerTest extends TestCase
{
    public function test_home_page_Route(): void
    {
        $this->mock(\App\Http\Controllers\XmlController::class, function ($mock) {
            $mock->shouldReceive('get_all_entries')
                 ->once()
                 ->andReturn([
                     [
                         'id' => 'ARO-1-0001-01',
                         'xml' => '<xml>...</xml>',
                         'inner_text' => 'Some transcription text...',
                         'volume' => '1',
                         'chapter' => '1',
                         'page' => '1',
                         'date' => '2024-12-01',
                         'type' => 'text',
                         'language' => 'latin'],
                     [
                         'id' => 'ARO-1-0001-02',
                         'xml' => '<xml>...</xml>',
                         'inner_text' => 'Another transcription...',
                         'volume' => '1',
                         'chapter' => '2',
                         'page' => '2',
                         'date' => '2024-12-02',
                         'type' => 'text',
                         'language' => 'latin'
                     ]
                 ]);

            $mock->shouldReceive('display_entries')
                 ->with([
                     [
                         'id' => 'ARO-1-0001-01',
                         'xml' => '<xml>...</xml>',
                         'inner_text' => 'Some transcription text...',
                         'volume' => '1',
                         'chapter' => '1',
                         'page' => '1',
                         'date' => '2024-12-01',
                         'type' => 'text',
                         'language' => 'latin'
                     ],
                     [
                         'id' => 'ARO-1-0001-02',
                         'xml' => '<xml>...</xml>',
                         'inner_text' => 'Another transcription...',
                         'volume' => '1',
                         'chapter' => '2',
                         'page' => '2',
                         'date' => '2024-12-02',
                         'type' => 'text',
                         'language' => 'latin'
                     ]
                 ])
                 ->once()
                 ->andReturn('displayed entries output');
        });

        $response = $this->get('/home');
        $response->assertStatus(200);
        $response->assertSee('displayed entries output');
    }
}