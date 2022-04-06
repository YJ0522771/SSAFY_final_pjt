<template>
  <div v-if="review">
    <div class="d-flex justify-content-center align-items-center">
      <img :src="getemo(review.vote)" alt="" class="emoimg align-self-start">
      <span class="fs-1 fw-bold">{{ review.title }}</span>
    </div>
    <hr>
    <div class="review-box d-flex justify-content-start align-items-center py-5">
      <img :src="movie.poster_path" alt="" class="posterimg">
      <div class="d-flex flex-column justify-content-between align-items-start h-100">
        <div class="d-flex mt-1">
          <span @click.prevent="goProfile" class="username">{{ review.username }} </span> 
          <div class="align-self-center">
            <i class="fas fa-star" style="color: yellow;"></i>
            <span style="color: aqua;"> {{ review.vote }}</span>
          </div>
        </div>
        
        <p class="mt-3 mx-3 review-content">{{ review.content }}</p>
        <div style="text-align: start;">
          <div class="d-flex  align-items-center" 
          v-if="review.username === username">
            <button class="btn btn-primary me-2" @click="goReviewRevise">
              <i class="fas fa-edit"></i> 수정</button>
            <button class="btn btn-danger" @click="reviewDelete">
            <i class="fas fa-eraser"></i> 삭제</button>
          </div>
          <p class="mt-4" style="font-size: 14px;">작성시간: {{ review.created_at | dateFilter }}</p>
        </div>
      </div>
      <div>
      </div>

    </div>
    
    <!-- <p>수정시간 : {{ review.updated_at | dateFilter }}</p> -->
    <hr>
    
    <CommentForm 
    :movie_id="Number(movie_id)"
    :review_id="Number(review_id)"
    @create-comment="getCommentList" />
    <br>
    <CommentList 
    :review_id="Number(review_id)"
    :comment_list="comment_list"
    @delete-comment="getCommentList" />
    <br>
    <br>
  </div>
</template>

<script>
// import "moment/locale/ko"
// import moment from 'moment'

import axios from 'axios'
import jwt_decode from "jwt-decode";

import CommentList from '@/components/CommentList.vue'
import CommentForm from '@/components/CommentForm.vue'

const SERVER_URL = process.env.VUE_APP_SERVER_URL

export default {
  name: 'ReviewDetail',
  components: {
    CommentList,
    CommentForm
  },
  data: function () {
    return {
      movie_id: null,
      movie: null,
      review_id: null,
      review: null,
      username: null,
      comment_list: [],
    }
  },
  created: function () {
    console.log('다시요청')
    this.getReview()
    this.getUserData()
    this.getCommentList()
    console.log(this.movie)
  },
  methods: {
    setToken: function () {
      const token = localStorage.getItem('jwt')
      const config= {
        Authorization: `JWT ${token}`
      }
      return config
    },
    getMovie: function () {
      if (!this.movie_id) {
        this.movie_id = this.review.movie_id
      }
      
      const MOVIE_URL = `${SERVER_URL}/movies/${this.movie_id}/`
      axios.get(MOVIE_URL)
        .then(res => {
          // console.log(res.data)
          this.movie = res.data

          // console.log(this.$router)
          // this.$router.push({
          //   name: 'MovieInfo',
          //   params: {
          //     id: this.movie_id,
          //     movie: this.movie
          //   }
          // })
        })
        .catch(error => {
          console.log(error)
          this.movie = null
        })
    },
    getReview: function () {
      if (!this.review_id) {
        this.review_id = this.$route.params.review_id
      }

      const REVIEW_URL = `${SERVER_URL}/community/${this.review_id}/detail/`
      // const REVIEW_URL = `${SERVER_URL}/community/3/detail/`

      axios.get(REVIEW_URL)
        .then(res => {
          this.review = res.data
          // this.getemo(this.review.vote)
          this.getMovie()
          console.log(this.getemo(this.review.vote))
          // console.log(this.review)
        })
        .catch(error => {
          console.log(error)
          this.review = null
        })
    },
    getUserData: function () {
      const token = localStorage.getItem('jwt')
      if (token) {
        let decoded = jwt_decode(token)
        this.username = decoded.username
      }
    },
    getemo: function (data) {
      let emo_poster = ""
      if (data < 3) {
        emo_poster = require("../../../public/emoticon/1_2.png")
      } else if (data < 5) {
        emo_poster = require("../../../public/emoticon/3_4.png")
      } else if (data < 7) {
        emo_poster = require("../../../public/emoticon/5_6.png")
      } else if (data < 9) {
        emo_poster = require("../../../public/emoticon/7_8.png")
      } else {
        emo_poster = require("../../../public/emoticon/9_10.png")
      }
      return emo_poster
    },
    goReviewRevise: function () {
      // console.log(this.review)
      this.$router.push({
        name: 'ReviewRevise', 
        query: {
            review_id: this.review_id,
            movie: this.movie
          }
      })
    },
    reviewDelete: function () {
      axios({
        method: 'delete',
        url: `${SERVER_URL}/community/${this.review.id}/putdelete/`,
        data: this.review,
        headers: this.setToken()
      })
        .then(res => {
          console.log(res)
          // this.movie_id = this.$route.params.id
          this.$router.push({name: 'ReviewList', 
              params: {
                id: this.movie_id,
            }
          }) 
        })
        .catch(err => {
          console.log(err)
        })
    },
    getCommentList: function () {
      const COMMENT_URL = `${SERVER_URL}/community/${this.review_id}/comment/`

      axios.get(COMMENT_URL)
        .then(res => {
          console.log(res)
          this.comment_list = res.data
        })
        .catch(error => {
          console.log(error)
          this.comment_list = []
        })
    },
    goProfile: function () {
      this.$router.push({
        name: 'Profile',
        params: {
          username: this.review.username
        }
      })
    }
  }
}
</script>

<style scoped>
  .username {
    cursor: pointer;
    margin: 2px 2px 2px 2px;
    font-size: 20px;
    margin-right: 1rem;
    font-weight: bold;
  }

  .username:hover {
    text-decoration-line: underline;
  }

  .starcolor {
    color: yellow;
  }

  .emoimg {
    width: 58px;
    margin-right: 20px;
  }

  .review-box {
    margin-right: 15vw;
    margin-left: 15vw;
    height: 40rem;
    
  }

  .posterimg {
    width: 20rem;
    margin-right: 30px;
  }

  .review-content {
    height: 20rem;
    width: 41rem;
    text-align: start;
  }

</style>