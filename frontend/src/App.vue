<template>
  <h1>記事スクレイピングツール</h1>
  <form method="POST">
    <div class="table-area">
      <div class="table-row">
        <div class="table-cell">対象サイト</div>
        <div class="table-cell">
          <input type="text" value="https://breezegroup.co.jp" disabled>
        </div>
      </div>
      <div class="table-row">
        <div class="table-cell">取得数</div>
        <div class="table-cell">
          <input type="number"
          min="1"
          v-model="state.articleCount"
          :disabled="state.allFlg">
          <label>
            <input type="checkbox"
            v-model="state.allFlg">全件取得する
          </label>
        </div>
      </div>
      <div class="table-row">
        <div class="table-cell">拡張子</div>
        <div class="table-cell">
          <select v-model="state.format">
            <option value="excel">excel</option>
            <option value="csv">csv</option>
          </select>
        </div>
      </div>
    </div>
    <div class="exec-area">
      <button
      @click="exec">実行</button>
    </div>
  </form>
  <a v-show="state.completeFlg"
    :href="state.filePath"
    download>ダウンロードする</a>
  <ModalView
    v-show="state.modalFlg"
    v-bind:startFlg="state.startFlg"
    v-bind:completeFlg="state.completeFlg"
    v-bind:max="state.max"
    v-bind:current="state.current"
    v-on:complete="complete"
  />
</template>

<script>
import { reactive } from '@vue/reactivity'
import ModalView from './components/ModalView.vue'
import { w3cwebsocket } from 'websocket'

export default {
  name: 'App',
  components: {
    ModalView
  },
  setup() {
    const state = reactive({
      modalFlg: false,
      allFlg: false,
      startFlg: false,
      completeFlg: false,
      btnFlg: true,
      format: 'excel',
      articleCount: 1,
      max:0,
      current:0,
      filePath: ''
    })

    const host = window.location.host;
    const ws = new w3cwebsocket(`ws://${host}/connection`);
    ws.onopen =  () => {
        console.log('Connected to chat.')
    }

    ws.onmessage = e => {
      const data = JSON.parse(e.data);
      switch (data.type) {
        case 'max':
          state.max = data.value;
          state.startFlg = true;
          break;
        case 'current':
          state.current += data.value;
          break;
        case 'complete':
          state.completeFlg = true;
          break;
        default:
          console.log(data.type)
          break;
      }
    }

    ws.onclose = () => {
      console.log('closed.');

    }

    ws.onerror = e => {
        console.log('error.');
        console.log(e);
    }

    const exec = e => {
      e.preventDefault();
      state.modalFlg = true;
      state.completeFlg = false;
      ws.send(JSON.stringify({
        number: state.articleCount,
        format: state.format,
        all: state.allFlg
      }))
    }
    const complete = () => {
      state.max = 0;
      state.current = 0;
      state.allFlg = false,
      state.modalFlg = false;
      state.startFlg = false;
      state.completeFlg = true;
      const fileFormat = state.format == 'excel' ? '.xlsx' : '.csv';
      state.filePath = `${window.location.origin}/static/result${fileFormat}`
    }

    return {
      state,
      exec,
      complete
    }
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}

.table-area {
  display: table;
  margin: 0 auto;
}

.table-row {
  display: table-row;
}

.table-cell {
  display: table-cell;
  text-align: left;
  padding: 1em;
}

.exec-area {
  margin-top: 1em;
}

.exec-area button {
  width: 20%;
  color: rgb(255, 255, 255);
  cursor: pointer;
  border-width: initial;
  border-style: none;
  border-color: initial;
  border-image: initial;
  background: rgb(100, 149, 237);
  border-radius: 10px;
}

</style>
