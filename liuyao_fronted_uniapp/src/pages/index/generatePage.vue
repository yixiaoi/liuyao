<template>

  
  <view class="container">

    <uni-section :title="'占问事项：'" type="line"></uni-section>
    <view class="uni-form-item uni-column">
      <input class="uni-input" maxlength="20" placeholder="请输入明确的求测内容" />
    </view>

    <!-- 单选控制 -->
    <uni-section title="时间选择模式" type="line">
      <view class="uni-px-5 uni-pb-5">
        <uni-data-checkbox v-model="mode" :localdata="modeOptions"></uni-data-checkbox>
      </view>
    </uni-section>
    

    <!-- 当选择 日期时间 时显示 -->
    <view v-if="mode === 'datetime'">
    <uni-section :title="'时间选择：' + datetimesingle" type="line"></uni-section>
		<view class="example-body">
			<uni-datetime-picker type="datetime" v-model="datetimesingle" @change="changeLog" />
		</view>
    </view>

    <!-- 当选择 月建日辰 时显示 -->
    <view v-if="mode === 'monthDay'">
        <uni-row class="demo-uni-row" :width="nvueWidth">
      <uni-col :span="12">
        
         <uni-section :title="'月建：'" type="line"></uni-section>

        <uni-data-select
          v-model="selectedMonthGan"
          :localdata="gan_range"
          emptyTips="天干"
          @change="onMonthGanChange"
        ></uni-data-select>

        <uni-data-select
          v-model="selectedMonthZhi"
          :localdata="zhi_range"
          emptyTips="地支"
          @change="onMonthZhiChange"
        ></uni-data-select>

      </uni-col>
      <uni-col :span="12">

        <uni-section :title="'日辰：'" type="line"></uni-section>

        <uni-data-select
          v-model="selectedDayGan"
          :localdata="gan_range"
          emptyTips="请选择天干"
          @change="onDayGanChange"
        ></uni-data-select>

        <uni-data-select
          v-model="selectedDayZhi"
          :localdata="zhi_range"
          emptyTips="请选择地支"
          @change="onDayZhiChange"
        ></uni-data-select>

      </uni-col>
    </uni-row>
    </view>

    <!-- 单选控制 -->
    <uni-section title="起卦选择模式" type="line">
      <view class="uni-px-5 uni-pb-5">
        <uni-data-checkbox v-model="guaMode" :localdata="guaModeOptions"></uni-data-checkbox>
      </view>
    </uni-section>

    <!-- 当选择 手动起卦 时显示 -->
    <view v-if="guaMode === 'manual'">
    <uni-section title="六爻选择" type="line">

      <uni-data-select
        v-model="yao_6"
        :localdata="range"
        emptyTips="请选择"
        @change="onChange6"
      ></uni-data-select>
      
      <uni-data-select
        v-model="yao_5"
        :localdata="range"
        emptyTips="请选择"
        @change="onChange5"
      ></uni-data-select>
            <uni-data-select
        v-model="yao_4"
        :localdata="range"
        emptyTips="请选择"
        @change="onChange4"
      ></uni-data-select>
            <uni-data-select
        v-model="yao_3"
        :localdata="range"
        emptyTips="请选择"
        @change="onChange3"
      ></uni-data-select>
            <uni-data-select
        v-model="yao_2"
        :localdata="range"
        emptyTips="请选择"
        @change="onChange2"
      ></uni-data-select>

        <uni-data-select
        v-model="yao_1"
        :localdata="range"
        emptyTips="请选择"
        @change="onChange1"
      ></uni-data-select>
    </uni-section>
    </view>

    <view class="uni-padding-wrap uni-common-mt">
      <button type="primary">开始起卦</button>
    </view>
      

  </view>


</template>

<script>

  export default {
    data() {
      return {
        mode: "datetime",
        guaMode: "manual",
        selectedMonthGan: '',
        selectedMonthZhi: '',
        selectedDayGan: '',
        selectedDayZhi: '',
        datetimesingle: '',
        yao_1: '',
        yao_2: '',
        yao_3: '',
        yao_4: '',
        yao_5: '',
        yao_6: '',


        modeOptions: [
        { value: "datetime", text: "日期时间" },
        { value: "monthDay", text: "月建日辰" }
      ],
      guaModeOptions: [
        { value: "manual", text: "手动起卦" },
        { value: "random", text: "随机起卦" }
      ],

        range: [
          { value: 0, text: "老阴 - - x" },
          { value: 1, text: "老阳 --- o" },
          { value: 2, text: "少阴 - - " },
          { value: 3, text: "少阳 --- " },
        ],
        gan_range: [
          { value: 0, text: "甲" },
          { value: 1, text: "乙" },
          { value: 2, text: "丙" },
          { value: 3, text: "丁" },
          { value: 4, text: "戊" },
          { value: 5, text: "己" },
          { value: 6, text: "庚" },
          { value: 7, text: "辛" },
          { value: 8, text: "壬" },
          { value: 9, text: "癸" },
        ],
        zhi_range: [
          { value: 0, text: "子" },
          { value: 1, text: "丑" },
          { value: 2, text: "寅" },
          { value: 3, text: "卯" },
          { value: 4, text: "辰" },
          { value: 5, text: "巳" },
          { value: 6, text: "午" },
          { value: 7, text: "未" },
          { value: 8, text: "申" },
          { value: 9, text: "酉" },
          { value: 10, text: "戌" },
          { value: 11, text: "亥" },
        ]
      };
    },
  methods: {
    onChange1(e) {
      console.log('选项一 changed:', e);
    },
    onChange2(e) {
      console.log('选项二 changed:', e);
    },
    onChange3(e) {
      console.log('选项三 changed:', e);
    },
    onChange4(e) {
      console.log('选项四 changed:', e);
    },
    onChange5(e) {
      console.log('选项五 changed:', e);
    },
    onChange6(e) {
      console.log('选项六 changed:', e);
    },
    onMonthGanChange(e) {
      console.log('天干 changed:', e);
    },
    onZhiChange(e) {
      console.log('地支 changed:', e);
    },
    onDayGanChange(e) {
      console.log('天干 changed:', e);
    },
    onDayZhiChange(e) {
      console.log('地支 changed:', e);
    }
  }
  };
</script>


<style scoped lang="scss">

  	/*每个页面公共css */
	/* uni.css - 通用组件、模板样式库，可以当作一套ui库应用 */
@import '@/common/uni.css';
@import '@/uni.scss';


.container {
  padding: 40rpx;
}

.title {
  font-size: $uni-font-size-sm;
  color: $uni-text-color;
   line-height: 36px;
}
</style>
