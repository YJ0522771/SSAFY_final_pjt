<template>
  <div v-if="movie">
    <div class="movie-info">
      <img :src="movie.poster_path" :alt="movie.title"
      class="poster">
      <div class="info">
        <p class="genre"> |
          <span
          v-for="(genre, idx) in movie.genres"
          :key="idx">
          {{ genre }} |
          </span>
        </p>
        <br>
        <p class="release-date">{{ getReleaseDate }}</p>
        <br>
        <hr>
        <!-- <p class="overview-title">줄거리</p> -->
        <p class="overview">{{ movie.overview }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

const SERVER_URL = process.env.VUE_APP_SERVER_URL

export default {
  name: 'MovieInfo',
  // props: {
  //   movie: Object,
  // },
  data: function () {
    return {
      movie: null
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
        })
        .catch(error => {
          console.log(error)
          this.movie = null
        })
    },
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
.movie-info {
  margin: 4rem auto;
  width: 70rem;
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
  font-size: 22px;
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
</style>