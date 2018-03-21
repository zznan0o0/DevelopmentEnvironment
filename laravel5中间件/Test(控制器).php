<?php namespace App\Http\Controllers;

use Illuminate\Http\Request;

class Test extends Controller{
  public function test(Request $request){
    $bbb = $request->input();
    return $bbb;
    // return shell_exec('python3 test.py');
  }
}