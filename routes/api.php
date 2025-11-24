<?php

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;

Route::prefix('v1')->group(function () {
    Route::post('arithmetic/add', [App\Http\Controllers\MathController::class, 'add']);
    Route::post('arithmetic/subtract', [App\Http\Controllers\MathController::class, 'subtract']);
    Route::post('arithmetic/multiply', [App\Http\Controllers\MathController::class, 'multiply']);
    Route::post('arithmetic/divide', [App\Http\Controllers\MathController::class, 'divide']);
    
    Route::post('algebra/solve-linear', [App\Http\Controllers\AlgebraController::class, 'solveLinear']);
    Route::post('algebra/solve-quadratic', [App\Http\Controllers\AlgebraController::class, 'solveQuadratic']);
    
    Route::post('matrices/operations', [App\Http\Controllers\MatrixController::class, 'operations']);
});
