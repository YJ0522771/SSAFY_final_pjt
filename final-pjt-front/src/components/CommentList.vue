<template>
  <div>
    <Comment 
    v-for="comment in comment_list"
    :key="comment.id"
    :comment="comment"
    :current_user="current_user" 
    @delete-comment="deleteComment" />
  </div>
</template>

<script>
import jwt_decode from "jwt-decode";
// import axios from 'axios'
import Comment from '@/components/Comment.vue'

// const SERVER_URL = process.env.VUE_APP_SERVER_URL

export default {
  name: 'CommentList',
  components: {
    Comment
  },
  props: {
    review_id: Number,
    comment_list: Array,
  },
  data: function () {
    return {
      current_user: ''
    }
  },
  created: function () {
    const token = localStorage.getItem('jwt')
    if (token) {
      let decoded = jwt_decode(token)
      this.current_user = decoded.username
    }
  },
  methods: {
    deleteComment: function () {
      this.$emit('delete-comment')
    }
  }
}
</script>

<style>

</style>