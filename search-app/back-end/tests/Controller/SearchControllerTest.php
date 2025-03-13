<?php

namespace Tests\Controllers;

use Tests\TestCase;
use App\Http\Controllers\SearchController;
use Illuminate\Http\Request;
use Mockery;

class SearchControllerTest extends TestCase {

    protected $searchController;
    protected $testSearch;

    public function setUp(): void {
        parent::setUp();

        $this->searchController = Mockery::mock(SearchController::class)->makePartial();
        $this->app->instance(SearchController::class, $this->searchController);

        $this->testSearch = [
            'query_type' => 'basic_search',
            'basicSearch' => 'test',
            'methodSearch' => 'keywords',
            'language' => 'la',
            'variant' => '1',
            'volumes' => ['1', '2', '4', '5', '6', '7', '8'],
            'pageSearch' => null,
            'entrySearch' => null,
            'startDate' => null,
            'endDate' => null,
            'docId' => null
        ];

        $this->searchController->shouldReceive('search')
            ->andReturn(response()->json([
                'success' => true,
                'num_results' => 1,
                'total_results' => 1,
                'results' => [
                    'ARO-1-0001-01' => [
                        'highlighted_html' => '<p>Test</p>',
                        'volume' => '1',
                        'page' => '1',
                        'date' => '1398-09-30'
                    ]
                ]
            ]));
    }

    protected function tearDown(): void {
        Mockery::close();
        parent::tearDown();
    }

    public function test_basic_search(): void {

        $request = new Request();
        $request->merge($this->testSearch);

        $response = $this->getJson('/api/search?' . http_build_query($this->testSearch));
        $response->assertStatus(200);
    }
}