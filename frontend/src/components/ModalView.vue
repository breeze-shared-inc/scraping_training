<template>
    <div class="modal">
        <div class="status-area"></div>
        <div>{{ state.message }}</div>
        <div v-show="startFlg">{{ current }} / {{ max }}</div>
        <ProgressBar
            v-bind:max="max"
            v-bind:current="current"
            v-bind:startFlg="startFlg"
        />
        <div>
            スクレイピング実行には数分〜数時間かかることがあります。<br>
            完了するまでお待ちください。
        </div>
    </div>
</template>


<script>
import ProgressBar from './ProgressBar.vue'
import { defineComponent, reactive } from '@vue/runtime-core';
export default defineComponent({
    name: 'ModalView',
    components: {
        ProgressBar
    },
    props: {
        startFlg: Boolean,
        completeFlg: Boolean,
        max: Number,
        current: Number
    },
    setup() {
        const state =  reactive({
            message: 'データ取得準備中...'
        })

        return {
            state
        }
    },
    watch: {
        startFlg() {
            this.state.message = 'データ取得中...'
        },
        current() {
            if (this.max <= this.current){
                this.state.message = 'データ生成中...'
            }
        },
        completeFlg() {
            this.$emit('complete',1)
        }
    }
})
</script>


<style scoped>
    .modal {
        width: 100vw;
        height: 100vh;
        position: fixed;
        top: 0px;
        left: 0px;
        vertical-align: middle;
        display: flex;
        flex-direction: column;
        justify-content: center;
        background: rgba(130, 167, 191, 0.8);
    }
    .status-area {
        margin-top: 1em;
    }
</style>