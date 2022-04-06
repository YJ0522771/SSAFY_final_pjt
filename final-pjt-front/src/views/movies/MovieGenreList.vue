<template>
  <div class="movie-list-form">
    <div v-for="(list, genre) in movieList"
    :key="genre"
    class="genre-list">
      <h3 class="genre-title">#{{ genre }}</h3>
      <div class="movie-list">
        <MovieCard 
        v-for="movie in list"
        :key="movie.id"
        :movie="movie"
        @movie_detail="getDetailId" />
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import MovieCard from '@/components/MovieCard.vue'

const SERVER_URL = process.env.VUE_APP_SERVER_URL

export default {
  name: 'MovieRandomList',
  components: {
    MovieCard,
  },
  data: function () {
    return {
      movieList: null,
    }
  },
  created: function () {
    this.getMovieList()
  },
  methods: {
    getMovieList: function () {
      const MOVIE_URL = `${SERVER_URL}/movies/genres/`
      axios.get(MOVIE_URL)
        .then(res => {
          console.log(res)
          this.movieList = res.data
        })
        .catch(error => {
          console.log(error)
          this.movieList = null
        })
    },
    getDetailId: function (data) {
      // console.log(data)
      this.$emit('movie_datail', data)
    }
  }
}
</script>

<style>
.genre-list {
  text-align: start;
}
</style>