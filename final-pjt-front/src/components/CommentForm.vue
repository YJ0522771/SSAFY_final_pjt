<template>
  <div class="commet-box">
    <h5>댓글 작성</h5>
    <div class="input-box">
      <input 
        type="text"
        v-model="input_text"
        class="comment-input"
      >
      <button 
      @click="createComment"
      class="input-box-btn btn btn-warning mx-2">등록</button>
    </div>

    {{ errMessage }}
  </div>
</template>

<script>
import axios from 'axios'

const SERVER_URL = process.env.VUE_APP_SERVER_URL

export default {
  name: 'CommentForm',
  props: {
    movie_id: Number,
    review_id: Number,
  },
  data: function () {
    return {
      input_text: '',
      errMessage: ''
    }
  },
  methods: {
    setToken: function () {
      const token = localStorage.getItem('jwt')
      const config= {
        Authorization: `JWT ${token}`
      }
      return config
    },
    createComment: function () {
      const COMMENT_URL = `${SERVER_URL}/community/${this.review_id}/comment/create/`
      const data = {
        content: this.input_text
      }

      axios({
        method: 'post',
        url: COMMENT_URL,
        data: data,
        headers: this.setToken()
      })
        .then(res => {
          console.log(res)

          this.$emit('create-comment')
          this.input_text = ''
          this.errMessage = ''
        })
        .catch(err => {
          console.log(err.response)
          this.errMessage = err.response.data
        })
    }
  }
}
</script>

<style scoped>
  .commet-box {
    margin-left: 25vw;
    margin-right: 25vw;
  }
  .comment-input {
    width: 80%;
    padding: .375rem .75rem;
    font-size: 1rem;
    border-radius: .25rem;
  }

  /* .input-box {
    position: relative;
  }

  .input-box-btn {
    position: absolute;
  } */
</style>