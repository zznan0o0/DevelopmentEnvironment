<?php

/*
|--------------------------------------------------------------------------
| Application Routes
|--------------------------------------------------------------------------
|
| Here is where you can register all of the routes for an application.
| It's a breeze. Simply tell Laravel the URIs it should respond to
| and give it the controller to call when that URI is requested.
|
*/

Route::get('/', 'BarcodeConstroller@home');

Route::post('/login', 'UserConstroller@UserLogin');

Route::post('/bar_code','bar_code_data@bar_code');

Route::post('/UploadExcel', 'BarcodeConstroller@uploadExcel');

Route::post('/UploadStorageTxt', 'WarehouseConstroller@UploadStorageTxt');
Route::post('/UploadDeliveryTxt', 'WarehouseConstroller@UploadDeliveryTxt');
Route::post('/SelectInWarehouse', 'WarehouseConstroller@SelectInWarehouse');
Route::post('/getParameterData', 'WarehouseConstroller@getParameterData');

Route::post('/SelectDetial', 'GlassDetial@SelectDetial');
Route::post('/updataDamagedGlass', 'GlassDetial@updataDamagedGlass');
Route::post('/UserLogin', 'UserConstroller@UserLogin');


Route::post('/GetFileList', 'BarcodeConstroller@getFileList');
Route::post('/DelFile', 'BarcodeConstroller@DelFile');

Route::post('/GetGlassDamagedPiecesData', 'GlassAlterController@getGlassDamagedPiecesData');

Route::get('/test', 'Test@test')->middleware('test');





