<template>
  <div class="profile">
    <div class="profile-top">
      <p class="profile-username">
        <i class="fas fa-user-circle" style="padding-right: 0.5rem;"></i>
        {{ username }}
      </p>
      <!-- <br> -->
      <!-- <p>선호 장르</p> -->
      <!-- <span
        v-for="(genre, idx) in userGenres"
        :key="idx">{{ genre }} </span> -->
      
      <div class="progress text-start genre-bar"
      v-if="userGenreNames.length">
        <div 
        v-for="(genre, idx) in userGenreNames"
        :key="idx"
        :class="getProgressColor(idx)" role="progressbar" 
        :style="getProgressStyle(idx)" :aria-valuenow="getProgressVal(idx)"
        aria-valuemin="0" aria-valuemax="100">
        {{ genre }} ({{ userGenrePercent[idx] }}%)</div>
      </div>
      <div class="progress text-start genre-bar" 
      v-else>
        <div class="progress-bar progress-bar-striped bg-secondary" role="progressbar" 
        style="width: 100%" aria-valuenow="100" 
        aria-valuemin="0" aria-valuemax="100">리뷰를 작성하지 않았습니다.</div>
      </div>

      <br>
      <p>작성한 리뷰: {{ moviesCount }}개</p>
    </div>
    
    <br>
    <hr>
    <br>
    <p class="profile-review-title">Reviews</p>
    <div class="profile-movie-list">
        <ProfileMovieCard 
        v-for="movie in userMovies"
        :key="movie.review"
        :movie="movie" 
        @go_review="goReview(movie, movie.review_id)"/>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import ProfileMovieCard from '@/components/ProfileMovieCard.vue'

const SERVER_URL = process.env.VUE_APP_SERVER_URL

export default {
  name: 'Profile',
  components: {
    ProfileMovieCard,
  },
  data: function () {
    return {
      username: null,
      userMovies: [],
      userGenreNames: [],
      userGenrePercent: [],
      // userReviewIds: null,
      moviesCount: null,
      colors: ['primary', 'success', 'warning', 'danger', 'secondary']
    }
  },
  created: function () {
    this.getProfile()
  },
  methods: {
    getProfile: function () {
      if (!this.username) {
        this.username = this.$route.params.username
      }
      
      const MOVIE_URL = `${SERVER_URL}/accounts/profile/${this.username}/`
      axios.get(MOVIE_URL)
        .then(res => {
          console.log(res)
          this.userMovies = res.data.user_movies
          this.userGenreNames = res.data.user_genre_names
          this.userGenrePercent = res.data.user_genre_percent
          // this.userReviewIds = res.data.user_review_ids
          this.moviesCount = res.data.movies_count
        })
        .catch(error => {
          console.log(error)
          this.username = null
        })
    },
    // goDetail: function (movie_id) {
    //   this.$router.push({
    //     name: 'MovieDetail',
    //     params: {
    //       id: movie_id
    //     }
    //   })
    // },
    getProgressStyle: function (idx) {
      return `width: ${this.userGenrePercent[idx]}%` 
    },
    getProgressVal: function (idx) {
      return this.userGenrePercent[idx]
    },
    getProgressColor: function (idx) {
      return `progress-bar progress-bar-striped bg-${this.colors[idx]}`
    },
    goReview: function (mid, rid) {
      // console.log('리뷰')
      this.$router.push({name: 'ReviewDetail', 
          params: {
            review_id: rid,
        },
        query: {
          movie: mid,
        }
      })
    }
  },
  computed: {
    
  }  
}
</script>

<style>
.profile {
  padding: 3rem;
  text-align: start;
}

.profile-top {
  background-color: rgb(85, 91, 100);
  padding: 1rem;
  padding-left: 2rem;
}

.genre-bar {
  height: 40px;
  margin: 1rem 0;
  width: 70rem;
  font-weight: bold;
  font-size: 18px;
  text-align: start;
}

.profile-movie-list {
  margin: 0 auto;
  margin-top: 1rem;
  padding: 0.5rem 0;
  display: flex;
  flex-wrap: wrap;
  text-align: center;
}

.profile-review-title {
  font-size: 36px;
  font-weight: 700;
}

.profile-username {
  font-size: 40px;
  font-weight: 900;
}
</style>