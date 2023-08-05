var mydata = [
    {name: '北京',value: '1' },{name: '天津',value: '1' },
    {name: '上海',value: '16' },{name: '重庆',value: '0' },
    {name: '河北',value: '0' },{name: '河南',value: '0' },
    {name: '云南',value: '0' },{name: '辽宁',value: '0' },
    {name: '黑龙江',value: '0' },{name: '湖南',value: '0' },
    {name: '安徽',value: '0' },{name: '山东',value: '1' },
    {name: '新疆',value: '0' },{name: '江苏',value: '5' },
    {name: '浙江',value: '4' },{name: '江西',value: '0' },
    {name: '湖北',value: '0' },{name: '广西',value: '0' },
    {name: '甘肃',value: '0' },{name: '山西',value: '0' },
    {name: '内蒙古',value: '0' },{name: '陕西',value: '0' },
    {name: '吉林',value: '0' },{name: '福建',value: '1' },
    {name: '贵州',value: '0' },{name: '广东',value: '0' },
    {name: '青海',value: '0' },{name: '西藏',value: '0' },
    {name: '四川',value: '0' },{name: '宁夏',value: '0' },
    {name: '海南',value: '0' },{name: '台湾',value: '0' },
    {name: '香港',value: '0' },{name: '澳门',value: '0' }
];
var optionMap = {
    backgroundColor: '#FFFFFF',
    title: {
        text: '全国汽车产业链分布地图',
        subtext: '',
        x:'center'
    },
    tooltip : {
        trigger: 'item'
    },

    //左侧小导航图标
    visualMap: {
        show : true,
        x: '50px',
        y: '400px',
        splitList: [
            {start: 0, end:0},{start: 1, end: 1},
            {start: 2, end:4},{start: 5, end: 15},
            {start: 15, end: 20}
        ],
        // 图例大小
        itemHeight:25,
        color: ['#FF4500', '#1E90FF','#00BFFF', '#FFFF00', '#F0FFFF']
    },

    //配置属性
    series: [{
        name: '单点布局的汽车零部件企业数量',
        type: 'map',
        mapType: 'china',
        roam: true,
        label: {
            normal: {
                show: true  //省份名称
            },
            emphasis: {
                show: true
            }
        },
        data:mydata  //数据
    }]
};
//初始化echarts实例
var myChart = echarts.init(document.getElementById('center'));

//使用制定的配置项和数据显示图表
myChart.setOption(optionMap);
//柱状图
option = {
    title: {
        text: '全国汽车产业链分布柱状图',
        subtext: '',
        x:'center'
    },
    tooltip: {
        trigger: 'axis',
        axisPointer: {
            type: 'shadow'
        }
    },
    grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
    },
    xAxis: [
        {
            type: 'category',
            data: ['北京', '天津', '上海', '江苏', '浙江', '福建', '山东'],

            axisTick: {
                alignWithLabel: true
            }
        }
    ],
    yAxis: [
        {
            type: 'value'
        }
    ],
    series: [
        {
            name: '单点布局的汽车零部件企业数量',
            type: 'bar',
            barWidth: '50%',
            data: [1, 1, 16, 5, 4, 1, 1],
            itemStyle:{
                normal:{
                    //柱状图数据显示
                    label: {
                      show:true,//开启
                        position:'top',//位置
                        textStyle:{
                          color:'black',//颜色
                            fontSize:16//字体大小
                        }
                    },
                    //柱状图颜色
                    color:function (param){
                        var colorList=['#FFFF00','#FFFF00','#FF4500','#1E90FF','#00BFFF','#FFFF00','#FFFF00'];
                        return colorList[param.dataIndex]
                }
            }}
        }
    ]
};
//初始化echarts实例
var Chart = echarts.init(document.getElementById('char'));

//使用制定的配置项和数据显示图表
Chart.setOption(option);