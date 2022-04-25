<template>
    <div class="main">
        <div class="unknown" v-show="!startFlg">
            <div class="progress_back">
                <div class="progress_front_unknown"></div>
            </div>
        </div>
        <div class="active">
            <div class="progress_back" v-show="startFlg">
                <div class="progress_front" :style="'width:' + state.progress + '%;'"></div>
            </div>
        </div>
    </div>
</template>

<script>
import { reactive } from '@vue/reactivity'
import { defineComponent } from '@vue/runtime-core';

export default defineComponent({
    name: 'ProgressBar',
    props: {
        max: Number,
        current: Number,
        startFlg: Boolean
    },
    setup() {
        const state = reactive({
            progress: 0,
        });

        return {
            state
        }
    },
    watch: {
        current() {
            this.state.progress = (this.current / this.max) * 100;
        }
    }
})
</script>


<style scoped>
/* プログレスバーのCSS引用：https://qiita.com/keisuke-okb/items/60a56677ec7e464f1790 */
.main {
    width: 80%;
    margin: 1em auto;
}
.progress_back {
    display: block;
    width: 100%;
    height: 7px;
    position: relative;
    background: rgb(204, 204, 204);
}
.progress_front{
    display: block;
    width: 0;
    height: 7px;
    background: #e31787;
    position: absolute;
    left: 0;
    top: 0;
    border-radius: 10px;
    transition: 0.5s ease-in-out;
    overflow: hidden;
}

.progress_front_unknown{
    display: block;
    width: 100%;
    height: 7px;
    background: #ccc;
    position: absolute;
    left: 0;
    top: 0;
    border-radius: 10px;
    transition: 0.5s ease-in-out;
    overflow: hidden;
}
.progress_front_unknown::before {
    position: absolute;
    content: '';
    display: inline-block;
    top: 0px;
    left: -48%;
    width: 50%;
    height: 7px;
    background-color: #e31787;
    animation: bar-unknown 3s ease-out infinite;
    border-radius: 50px;
}
@keyframes bar-unknown {
    0% { transform: translateX(0%); }
    45% { transform: translateX(294%); }
    50% { transform: translateX(294%); }
    98% { transform: translateX(0%); }
    100% { transform: translateX(0%); }
}
</style>