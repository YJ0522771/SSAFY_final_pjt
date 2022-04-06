<template>
  <div class="comment-box">
    <div class=" d-flex justify-content-between align-items-center">
      <div class="d-flex flex-column align-items-start">
        <div>
          <span class="fw-bold mb-3">{{ comment.username }}</span>
          <span class="fw-light mx-3" style="font-size: 12px;">{{comment.created_at | dateFilter }}</span>
        </div>
        
        <span class="mt-3 mx-3" style="font-size: 16px;">{{ comment.content }}</span>
        
      </div>
      <button
        v-if="getSameUser"
        @click="deleteComment"
        class="btn btn-outline-danger px-2 py-1" style="font-size: 10px; margin-top: 0; margin-bottom: auto;"
      >X</button>
    </div>
    <hr>
  </div>
</template>

<script>
import axios from 'axios'

const SERVER_URL = process.env.VUE_APP_SERVER_URL

export default {  
  name: 'Comment',
  props: {
    comment: Object,
    current_user: String,
  },
  data: function () {
    return {
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
    deleteComment: function () {
      const URL = `${SERVER_URL}/community/comment/${this.comment.id}/delete/`

      axios({
        method: 'delete',
        url: URL,
        headers: this.setToken()
      })
        .then(res => {
          console.log(res)

          this.$emit('delete-comment')
          this.errMessage = ''
        })
        .catch(err => {
          console.log(err.response)
          this.errMessage = err.response.data
        })

    }
  },
  computed: {
    getSameUser: function () {
      return this.current_user === this.comment.username
    }
  }
}
</script>

<style scoped>
  .comment-box {
    margin-left: 20vw;
    margin-right: 20vw;
  }


</style>