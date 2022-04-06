<template>
  <div class="my-col">
    <div 
    class="h-100 my-card"
    @click="gotoDetail"
    @mouseover="visible"
    @mouseout="nonVisible">
      <img 
      :src="movie.poster_path" 
      class="list-poster" 
      :alt="movie.title"
      >

      <div class="wrap"
      v-show="textVisible">
        <h5 class="list-title">{{ movie.title }}</h5>
        <p class="list-vote">
          <i class="fas fa-star m-2 card-star"
          v-if="movie.vote_average >= 7.5"></i> 
          <i class="fas fa-star-half-alt m-2 card-star"
          v-else-if="movie.vote_average >= 5"></i> 
          <i class="far fa-star m-2 card-star"
          v-else></i>
          <span class="list-vote_avg">{{ movie.vote_average }}</span></p>
        <div> |
          <span
          v-for="(genre, idx) in movie.genres"
          :key="idx"
          class="list-genre">
          {{ genre }} |
          </span> 
        </div>
      </div>
    </div>
  </div>
</template>

<script>

export default {
  name: 'MovieCard',
  props: {
    movie: Object,
  },
  data: function () {
    return {
      textVisible: false,
    }
  },
  created: function () {

  },
  methods: {
    visible: function () {
      // console.log('over')
      this.textVisible = true
    },
    nonVisible: function () {
      // console.log('out')
      this.textVisible = false
    },
    gotoDetail: function () {
      this.$emit('movie_detail', this.movie.id)
    }
  },
  computed: {
  }
}

</script>

<style>
.my-col {
  margin: 1rem 1rem 1rem 0;
}

.my-card {
  position: relative;
  text-align: center;
  margin: 0;
  cursor: pointer;
  width: 14rem;
  height: 21rem;
}

.list-poster {
  display: block;
  width: 14rem;
  height: 21rem;
  border-radius: 5px;
}

.wrap {
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  right: 0;
  padding: 25px;
  color: #fff;
  background-color: rgba(0,0,0,0.5);
  border-radius: 5px;

  display: flex;
  flex-direction: column;
  justify-content: center;
}

.list-title {
  font-weight: bold;
}

.list-vote {
  font-size: 14px;
}

.list-vote_avg {
  color: aqua;
  font-size: 20px;
}

.card-star {
  color: yellow;
}
</style>