<template>
  <div>
    <div class="d-flex align-items-center justify-content-center">
      <!-- <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-search" viewBox="0 0 16 16">
        <path d="M11.742 10.344a6.5 6.5 0 1 0-1.397 1.398h-.001c.03.04.062.078.098.115l3.85 3.85a1 1 0 0 0 1.415-1.414l-3.85-3.85a1.007 1.007 0 0 0-.115-.1zM12 6.5a5.5 5.5 0 1 1-11 0 5.5 5.5 0 0 1 11 0z"/>
      </svg> -->
      <i class="fas fa-search fa-2x search-icon"></i>
      <input type="text" v-on:input="searchMovie" 
        v-model="searchInput"
        @keypress.enter="getMovieId"
        class="searchinput"
        placeholder="영화검색"
      >
    </div>
    <div v-if="searchMovieList" class="d-flex flex-column align-items-center justify-content-center">
      <div v-for="(movie, idx) in searchMovieList" :key=idx
        class="searchbar" @click="goDetail(movie.id)">
        <span class ="text text-start">{{movie.title}}</span>
      </div>
    </div>
    <div class="sub-nav">
      <router-link :to="{ name: 'MoviePlayingList' }">Now Playing</router-link> |
      <router-link :to="{ name: 'MovieGenreList' }">For Genre</router-link> |
      <router-link :to="{ name: 'MovieRandomList' }">Random</router-link>
    </div>
    <router-view 
    @movie_datail="goDetail" />
  </div>
</template>

<script>
import * as Hangul from 'hangul-js';
import axios from 'axios'

const SERVER_URL = process.env.VUE_APP_SERVER_URL
// const MOVIE_URL = 'http://127.0.0.1:8000/movies/'

export default {
  name: 'MovieList',
  data: function () {
    return {
      movieList: [],
      searchInput: '',
      searchMovieList: null,
      // detailMovieId: null,
    }
  },
  created: function () {
    this.getMovieList()
    this.$router.push({name: 'MoviePlayingList'})
  },
  methods: {
    goDetail: function (data) {
      // console.log(data)
      this.$emit('movie_datail', data)
      // this.$router.push({
      //   name: 'MovieDetail',
      //   params: {
      //     id: data,
      //   }
      // })
    },
    getMovieList: function () {
      const MOVIE_URL = `${SERVER_URL}/movies/all/`
      axios.get(MOVIE_URL)
        .then(res => {
          console.log(res)
          this.movieList = res.data
        })
        .catch(error => {
          console.log(error)
          this.movieList = []
        })
    },
    searchMovie: function (res) {
      const Input = Hangul.disassemble(res.target.value)
      if (res.target.value) {
        this.searchMovieList = this.movieList.filter((movie) => {
          const title = Hangul.disassemble(movie.title)
          let count = true
          for (let search in Input) {
            if (search < title.length ) {
              if (! (title[search] === Input[search])) {
                count = false
                break
              }
            }
            else {
              count = false
            }
          }
          return count
        })
        this.searchMovieList = this.searchMovieList.slice(0,9).sort(function (a, b) {
          return  a.title < b.title ? -1 : a.name > b.name ? 1 : 0;
        })
        console.log(this.searchMovieList)
      } else {
        this.searchMovieList = null
      }
    },
    // changeSearchInput: function (movie) {
    //   this.searchInput = movie.title
    //   this.searchMovieList = null
    // },
    getMovieId: function () {
      // let movieId = null
      for (let movie in this.searchMovieList) {
        if (this.searchInput === this.searchMovieList[movie].title) {
          let movieId = this.searchMovieList[movie].id
          this.goDetail(movieId)
        }
      }
    }
  }
}
</script>

<style>

.sub-nav {
  margin: 1rem;
  margin-top: 2rem;
}

.sub-nav a {
  font-weight: bold;
  font-size: 20px;
  color: rgb(243, 255, 250);
  text-decoration: none;
}

.sub-nav a.router-link-exact-active {
  color: red;
}

.searchinput {
  width: 50%;
  height: 46px;
  line-height: 46px;
  border: none;
  border-radius: 30px;
  padding: 10px;
}
.searchinput {
  width: 50%;
  height: 46px;
  line-height: 46px;
  border: none;
  border-radius: 30px;
  padding: 23px;
}

.searchbar {
  width: 48%;
  text-align: start;
  padding-left: 5px;
  margin-left: 3rem;
  background-color: white;
}

.searchbar:hover {
  cursor: pointer;
  background-color: gray;
}

.text {
  color: black;
}

.search-icon {
  padding: 0 0.5rem;
}
</style>