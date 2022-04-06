<template>
  <div class="box">
    <div class="d-flex justify-content-center">
      <img :src="movie.poster_path" alt="" class="poster-img">
      <img :src="movie.poster_path" alt="" class="poster-img">
      <img :src="movie.poster_path" alt="" class="poster-img">
    </div>
    <div class="create-box">
      <h3 class="mt-3">Review 작성</h3>
      <div>
        <h4>{{reviewData.vote}}점</h4>
        <div class="d-flex justify-content-center ">
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
          <input type="text" v-model="reviewData.title" class="titlebox form-control" 
          placeholder="리뷰 제목 (30자 이내)" maxlength="30">
        </div>
        <p class="text-danger mt-1 mb-1">{{errMessageTitle}}</p>
        <div>
          <textarea name="" id="" cols="30" rows="5" v-model="reviewData.content" 
            class="contentbox form-control" placeholder="감상평을 남겨주세요 (500자 이내)" maxlength="500">
          </textarea>
        </div>
        <p class="text-danger mt-1 mb-1">{{errMessageContent}}</p>
        <button @click="reviewCreate" class="btn">작성하기</button>
      </div>  
      
      
    </div>
    
  </div>
</template>

<script>
import axios from 'axios'

const SERVER_URL = process.env.VUE_APP_SERVER_URL

export default {
  name: 'ReviewCreate',
  data: function () {
    return {
      movie_id: null,
      movie: null,
      errMessageTitle: '',
      errMessageContent: '',
      reviewData: {
        title: null,
        content: null,
        vote: 5,
      },
      starList: [1,1,1,1,1,0,0,0,0,0]
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
    reviewCreate: function () {
      axios({
        method: 'post',
        url: `${SERVER_URL}/community/${this.movie_id}/create/`,
        data: this.reviewData,
        headers: this.setToken()
      })
        .then(res => {
          console.log(res)
          this.errMessage = ''
          this.$router.push({
            name: 'ReviewList',
            params: {
              id: this.movie_id
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
    checkstar: function (idx) {
      for (let i=0; i< 10; i++) {
        if (i <= idx) {
          this.starList[i] = 1
        } else {
          this.starList[i] = 0
        }
      }
      this.reviewData.vote = idx+1
      this.starList = this.starList.splice(0,10)
    },
  },
  created: function () {
    this.movie_id = this.$route.query.movie_id
    console.log(this.$route.query.movie)
    if (this.$route.query.movie.id) {
      this.movie = this.$route.query.movie
    } else {
      this.$router.push({name: 'MovieDetail', 
        params: {
          id: this.movie_id
        }
      })
    }
  },
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