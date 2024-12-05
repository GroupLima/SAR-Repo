<?php

namespace Tests\Controllers;

use Tests\TestCase;

class RouteControllerTest extends TestCase
{
    public function test_home_page(): void
    {
        // Send a GET request to the home page
        $response = $this->get('/');

        // Assert that the response status is 200 (successful)
        $response->assertStatus(200);

        // Assert that the response contains the text
        $response->assertSee('Discover 8 Volumes');
    }

    public function test_about_page(): void
    {
        $response = $this->get('/about');
        $response->assertStatus(200);
        $response->assertSee('IMPORTANT LINKS');
    }
    
    public function test_search_page(): void
    {
        $response = $this->get('/xquery');
        $response->assertStatus(200);
        $response->assertSee('search');
    }
}