<template>
  <div class="d-flex justify-content-center" v-if="movie">
    <img :src="movie.poster_path" alt="" class="community-poster">
    <div>
      <h3>Reviews</h3>
      <button
      class="btn review-create-btn"
      @click="goReviewCreate">리뷰 작성</button>
      
      <hr style="width: 58rem; margin: 1rem auto;">

      <div v-if="review_exist"
      class="review-list-form">
        <table class="table text-center review-table">
          <thead>
            <tr>
            <th scope="col" class="col-1">#</th>
            <th scope="col" class="col-6">제목</th>
            <th scope="col" class="col-1"><i class="fas fa-star"></i></th>
            <th scope="col" class="col-2">작성자</th>
            <th scope="col" class="col-2">작성시간</th>
            </tr>
          </thead>
          <Review
          v-for="review in review_list"
          :key="review.id"
          :review="review"
          @review-detail="goReviewDetail(review.id)" />
        </table>
      </div>
      <div v-else>
        <p>이 영화의 첫 리뷰를 남겨주세요.</p>
      </div>
      
      <button
      class="commu-btn btn btn-warning"
      @click="goMovieDetail">영화정보 바로가기</button>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import Review from '@/components/Review.vue'

const SERVER_URL = process.env.VUE_APP_SERVER_URL

export default {
  name: 'ReviewList',
  components: {
    Review,
  },
  data: function (){
    return {
      movie_id: null,
      movie: null,
      review_list: [],
      review_exist: true,
    }
  },
  created: function () {
    this.getReviews()
    this.getMovie()
  },
  methods: {
    getMovie: function () {
      if (!this.movie_id) {
        this.movie_id = this.$route.params.id
      }
      
      const MOVIE_URL = `${SERVER_URL}/movies/${this.movie_id}/`
      axios.get(MOVIE_URL)
        .then(res => {
          // console.log(res)
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
    getReviews: function () {
      if (!this.movie_id) {
        this.movie_id = this.$route.params.id
      }
      
      const REVIEW_URL = `${SERVER_URL}/community/${this.movie_id}/`
      // const REVIEW_URL = `${SERVER_URL}/community/3/`
      axios.get(REVIEW_URL)
        .then(res => {
          // console.log(res)
          this.review_list = res.data
          if (!this.review_list.length) {
            this.review_exist = false
          }
        })
        .catch(error => {
          console.log(error)
          this.review_list = []
        })
    },
    goReviewDetail: function (data) {
      console.log(data)
      this.$router.push({name: 'ReviewDetail', 
          params: {
            review_id: data,
        },
      })
    },
    goReviewCreate: function () {
      this.$router.push({name: 'ReviewCreate', query: {
          movie_id: this.movie_id,
          movie: this.movie,
        }
      })
    },
    goMovieDetail: function () {
      this.$router.push({
        name: 'MovieDetail',
        params: {
          id: this.movie_id
        }
      })
    }
  }
}
</script>

<style scoped>
.review-table {
  color: white;
  text-align: center;
}

.review-table th {
  font-size: 16px;
  padding: 1rem;
}

.review-list-form {
  width: 55rem;
  margin: auto;
  text-align: center;
}

.review-box {
  padding: 2rem;
}

.community-poster {
  width: 30rem;
  margin: 0 2rem;
}

.commu-btn {
  width: 50%;
  margin-top: 5rem;
}

.review-create-btn {
  font-weight: bold;
  background-color: yellowgreen;
  
}

.review-create-btn:hover{
  background-color: rgb(181, 243, 58)
}

/* .list-box {
  position: relative;
}

.img-opacity {
  opacity: 0.1;
}

.review-box {
  position: absolute;
  background-color: rgb(32, 37, 44);
  top: 50%;
	left: 50%;
	transform: translate( -50%, -50% );
} */
</style>