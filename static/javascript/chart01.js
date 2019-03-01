// 圖表配置
var options = {
    chart: {
        type: 'bar'                          //指定圖表的類型，默認是折線圖（line）
    },
    title: {
        text: '主標題-我的第一個圖表'                 // 標題
    },
    subtitle: {
        text: '副標題-沒有人愛車000000'
    },
    xAxis: {
        categories: ['蘋果', '香蕉', '橙子']   // x 軸分類
    },
    yAxis: {
        title: {
            text: '吃水果個數'                // y 軸標題
        }
    },
    series: [{                              // 數據列
        name: '小明000',                        // 數據列名
        data: [1, 8, 15]                     // 數據
    }, {
        name: '小紅',
        data: [9, 15, 7]
    }]
};
// 圖表初始化函數
var chart = Highcharts.chart('container', options);
