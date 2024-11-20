<?php

namespace Tests\Controllers;

use Tests\TestCase;

class RouteControllerTest extends TestCase
{
    // Test the home page route
    public function test_Route_display_view_home_page(): void
    {
        $this->mock(\App\Services\XmlController::class, function ($mock) {
            $mock->shouldReceive('get_all_entries')
                 ->once()
                 ->andReturn(['entry1', 'entry2']);
                 
            $mock->shouldReceive('display_entries')
                 ->with(['entry1', 'entry2'])
                 ->once()
                 ->andReturn('displayed entries output');
        });

        $response = $this->get('/home');
        $response->assertStatus(200);
        $response->assertSee('displayed entries output');
    }

    // Test a valid page
    public function test_Route_display_view_valid_non_home_page(): void
    {
        $response = $this->get('/about');
        $response->assertStatus(200);
        $response->assertViewIs('about');
    }

    // Test an invalid page route
    public function test_Route_display_view_invalid_page(): void
    {
        $response = $this->get('/invalid-page');
        $response->assertStatus(404);
    }
}
