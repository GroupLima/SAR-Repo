<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Validation\ValidationException;
use Illuminate\Support\Facades\Log;
use Illuminate\Support\Facades\Http;
use Symfony\Component\Process\Process;


class TestController extends Controller
{
    public function test(Request $request)
    {
        Log::info('Test API route hit');
        return response()->json(['success' => true]);
    }
}