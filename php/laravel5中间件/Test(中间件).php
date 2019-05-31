<?php
//中间件
namespace App\Http\Middleware;

use Closure;

class Test
{
    /**
     * Handle an incoming request.
     *
     * @param  \Illuminate\Http\Request  $request
     * @param  \Closure  $next
     * @return mixed
     */
    public function handle($request, Closure $next)
    {   
        $mid_args = ['a' => 1, 'b' => 2];
        $res = ['b' => 1, 'c' => 2];
        //将中间件想要传的数据合并到请求数据中
        $request->merge($mid_args);
        //这样可以直接返回到前端
        return response($res);
        //这样讲数据传给控制器
        return $next($request);
    }
}
