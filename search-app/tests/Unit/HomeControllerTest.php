<?php

namespace Tests\Controllers;

use Tests\TestCase;

class HomeControllerTest extends TestCase
{
    // test the home page returns a successful response
    public function test_home_page(): void
    {
        // Send a GET request to the home page
        $response = $this->get('/');

        // Assert that the response status is 200 (successful)
        $response->assertStatus(200);

        // Assert that the response contains the text
        $response->assertSee('SAR');
    }
}

