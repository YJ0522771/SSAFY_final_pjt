<template>
  <div class="box" v-if="review">
    <div class="d-flex justify-content-center">
      <img :src="movie.poster_path" alt="" class="poster-img">
      <img :src="movie.poster_path" alt="" class="poster-img">
      <img :src="movie.poster_path" alt="" class="poster-img">
    </div>
    <div class="create-box">
      <h3 class="mt-3">Review 수정</h3>
      <div>
        <h4>{{review.vote}}점</h4>
        <div class="d-flex justify-content-center">
          <div v-for="(star, idx) in starList" :key="idx" @click="checkstar(idx)" class="starcolor">
            <div v-if="star">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-star-fill starcolor" viewBox="0 0 16 16">
                <path d="M3.612 15.443c-.386.198-.824-.149-.746-.592l.83-4.73L.173 6.765c-.329-.314-.158-.888.283-.95l4.898-.696L7.538.792c.197-.39.73-.39.927 0l2.184 4.327 4.898.696c.441.062.612.636.282.95l-3.522 3.356.83 4.73c.078.443-.36.79-.746.592L8 13.187l-4.389 2.256z"/>
              </svg>
            </div>
            <div v-else>
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-star starcolor" viewBox="0 0 16 16">
                <path d="M2.866 14.85c-.078.444.36.791.746.593l4.39-2.256 4.389 2.256c.386.198.824-.149.746-.592l-.83-4.73 3.522-3.356c.33-.314.16-.888-.282-.95l-4.898-.696L8.465.792a.513.513 0 0 0-.927 0L5.354 5.12l-4.898.696c-.441.062-.612.636-.283.95l3.523 3.356-.83 4.73zm4.905-2.767-3.686 1.894.694-3.957a.565.565 0 0 0-.163-.505L1.71 6.745l4.052-.576a.525.525 0 0 0 .393-.288L8 2.223l1.847 3.658a.525.525 0 0 0 .393.288l4.052.575-2.906 2.77a.565.565 0 0 0-.163.506l.694 3.957-3.686-1.894a.503.503 0 0 0-.461 0z"/>
              </svg>
            </div>
          </div>
        </div>
      </div>
      <p>별점을 선택하세요</p>
      <div>
        <div>
          <input type="text" v-model="review.title" class="titlebox form-control" maxlength="30">
        </div>
        <p class="text-danger mt-1 mb-1">{{errMessageTitle}}</p>
        <div>
          <textarea name="" id="" cols="30" rows="5" v-model="review.content" 
            class="contentbox form-control" maxlength="500">
          </textarea>
        </div>
        <p class="text-danger mt-1 mb-1">{{errMessageContent}}</p>
        <button @click="reviewPut" class="btn">수정하기</button>
      </div>  
      
    </div>
  </div>
</template>

<script>
import axios from 'axios'

const SERVER_URL = process.env.VUE_APP_SERVER_URL

export default {
  name: 'ReviewRevise',
  data: function () {
    return {
      movie: null,
      review_id: null,
      review: null,
      errMessageTitle: '',
      errMessageContent: '',
      starList: [0,0,0,0,0,0,0,0,0,0]
    }
  },
  created: function (){
    this.getReview()
    
  },
  methods: {
    setToken: function () {
      const token = localStorage.getItem('jwt')
      const config= {
        Authorization: `JWT ${token}`
      }
      return config
    },
    getReview: function () {
      if (!this.review_id) {
        this.review_id = this.$route.query.review_id
      }
      const REVIEW_URL = `${SERVER_URL}/community/${this.review_id}/detail/`
      // const REVIEW_URL = `${SERVER_URL}/community/3/detail/`
      axios.get(REVIEW_URL)
        .then(res => {
          this.review = res.data
          if (this.$route.query.movie.id) {
            this.movie = this.$route.query.movie
          } else {
            this.$router.push({name: 'ReviewList', 
                params: {
                  id: this.review.movie_id,
              }
            })
          }
          this.getStar()
        })
        .catch(error => {
          console.log(error)
          this.review = null
        })
    },
    getStar: function () {
      console.log(this.review.vote)
      for (let i=0; i < this.review.vote; i++) {
        this.starList[i] = 1
      }
    },
    checkstar: function (idx) {
      for (let i=0; i < 10; i++) {
        if (i <= idx) {
          this.starList[i] = 1
        } else {
          this.starList[i] = 0
        }
      }
      console.log(this.review.vote)
      this.review.vote = idx+1
      this.starList = this.starList.splice(0,10)
    },
    reviewPut: function () {
      axios({
        method: 'put',
        url: `${SERVER_URL}/community/${this.review.id}/putdelete/`,
        data: this.review,
        headers: this.setToken()
      })
        .then(res => {
          console.log(res)
          this.errMessage = ''
          this.$router.push({name: 'ReviewDetail', 
            params: {
              review_id: this.review.id,
            },
            query: {
              movie: this.movie,
            }
          })
        })
        .catch(err => {
          // console.log(err.response)
          if (err.response.data.title) {
            this.errMessageTitle = '제목을 입력해주세요.'
          }

          if (err.response.data.content) {
            this.errMessageContent = '내용을 입력해주세요.'
          }
        })
    },
    
  }
}
</script>

<style scoped>
  .box {
    position: relative;
    /* margin: 0 35vw 0 35vw; */
    padding: 20px 10px 20px 10px;
  }

  .create-box {
    position: absolute ;
    top: 50%;
    left: 50%;
    transform: translate( -50%, -50% );
    width: 50vw;
    height: 60vh;
    padding: 60px 68px 40px;
    background-color: rgb(32, 37, 44);
    border-radius: 4px;
  }

  .starcolor {
    color: yellow;
    
  }

  .titlebox {
    margin-bottom: 10px;
    width: 100%;
    border-radius: 4px;
  }

  .contentbox {
    width: 100%;
    border-radius: 4px;
    margin-bottom: 10px;
  }

  .btn {
    background-color: yellow;
    width: 100%;
  }

  .poster-img {
    opacity: 0.5;
  }
  
</style>