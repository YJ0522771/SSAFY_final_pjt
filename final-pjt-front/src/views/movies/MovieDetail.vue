<template>
  <div v-if="movie" class="movie-box">
    <!-- <div class="sub-nav">
      <router-link :to="{ name: 'ReviewList',
        params: {
          id: movie_id,
        } }"
      ></router-link> 
    </div> -->
    <div class="movie-info" id="movieinfo" >
      <img :src="movie.poster_path" :alt="movie.title"
      class="poster">
      <div class="info">
        <p class="detail-movie-title">{{ movie.title }}</p>
        <p class="genre"> |
          <span
          v-for="(genre, idx) in movie.genres"
          :key="idx">
          {{ genre }} |
          </span>
        </p>
        <div class="detail-movie-vote">
          <i class="fas fa-star" style="color: yellow;"
          v-if="movie.vote_average >= 7.5"></i>
          <i class="fas fa-star-half-alt" style="color: yellow;"
          v-else-if="movie.vote_average >= 5"></i> 
          <i class="far fa-star" style="color: yellow;"
          v-else></i>
          <span> {{ movie.vote_average }}</span>
        </div>
        
        <br>
        <p class="release-date">{{ getReleaseDate }}</p>
        <br>
        <hr>
        <!-- <p class="overview-title">줄거리</p> -->
        <p class="overview">{{ movie.overview }}</p>
        <button class="review-btn btn btn-warning" @click="goReviewList">커뮤니티 바로가기</button>
      </div>
    </div>

      
    <router-view/>
  

    <!-- <MovieInfo 
    :movie="movie" />
    <hr>
    <ReviewList /> -->
  </div>
</template>

<script>
import axios from 'axios'
// import MovieInfo from '@/components/MovieInfo.vue'
// import ReviewList from '@/components/ReviewList.vue'

const SERVER_URL = process.env.VUE_APP_SERVER_URL

export default {
  name: 'MovieDetail',
  components: {
    // MovieInfo,
    // ReviewList,
  },
  data: function () {
    return {
      movie_id: null,
      movie: null,
      reviews: null,
    }
  },
  created: function () {
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
          console.log(res)
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
    goReviewDetail: function (data) {
      this.$router.push({
        name: 'ReviewDetail',
        params: {
          id: this.movie_id,
          review_id: data
        }
      })
    },
    goReviewList: function () {
      this.$router.push({name: 'ReviewList', 
          params: {
            id: this.movie_id,
        }
      })
    }
  },
  computed: {
    getReleaseDate: function () {
      let data = ''
      for (let i = 0; i < 10; i++) {
        if (i === 4 || i === 7){
          continue
        }
        data += this.movie.release_date[i]
        if (i === 3){
          data += '년 '
        } else if (i === 6) {
          data += '월 '
        } 
      }
      data += '일 개봉'
      return data
    }
  }
}

</script>

<style>
.movie-box {
  padding: 20px 20px 20px 20px;
}

.detail-movie-title {
  font-size: 36px;
  font-weight: 900;
  padding: 0 1rem;
}

.detail-movie-vote {
  font-size: 22px;
  font-weight: 700;
  color: aqua;
  padding: 0 1rem;
}

.movie-info {
  width: 70rem;
  margin: 1rem auto;
  display: flex;
  justify-content: start;

  background-clip: border-box;
  border: 1px solid rgba(255, 255, 255, 0.767);
  border-radius: .25rem
}

.poster {
  width: 40%;
}

.info {
  padding: 3rem;
  text-align: start;
}

.info .genre {
  padding: 0 1rem;
  font-size: 24px;
  font-weight: 900;
  color: antiquewhite;
}

.release-date {
  margin: 0;
  padding: 0 1rem;
  font-size: 18px;
}

.overview-title {
  margin: 0;
  padding: 3rem 0 0 1rem;
  font-size: 24px;
  font-weight: 900;
}

.overview {
  margin: 0;
  padding: 3rem 1rem;
  font-size: 16px;
  color: white;
}

.review-btn {
  width: 100%;
}
</style>