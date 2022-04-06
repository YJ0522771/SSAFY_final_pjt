<template>
  <div class="my-col">
    <div 
    class="h-100 my-card"
    @click="goReview"
    @mouseover="visible"
    @mouseout="nonVisible">
      <img 
      :src="movie.poster_path" 
      class="list-poster" 
      :alt="movie.title"
      >

      <div class="wrap"
      v-show="textVisible">
        <!-- <p>My Review</p> -->
        <h5 class="profile-title">{{ movie.review_title }}</h5>
        <!-- <p>영화: {{ movie.title }}</p> -->
        <p class="profile-vote">
          <i class="fas fa-star m-2" style="color: yellow;"></i> 
          <span class="list-vote_avg">{{ movie.review_vote }}</span>
        </p>
        <p>작성일: {{ getDate }}</p>
      </div>
    </div>
  </div>
</template>

<script>

export default {
  name: 'ProfileMovieCard',
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
    goReview: function () {
      this.$emit('go_review')
    }
  },
  computed: {
    getDate: function () {
      if (!this.movie) {
        return ''
      }
      let data = ''
      for (let i = 0; i < 10; i++) {
        if (i === 4 || i === 7){
          continue
        }
        data += this.movie.review_created[i]
        if (i === 3){
          data += '-'
        } else if (i === 6) {
          data += '-'
        } 
      }
      return data
    }
  }
}

</script>

<style>
.my-col {
  margin: 1rem 0;
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

.profile-title {
  font-weight: bold;
}

.profile-vote {
  font-size: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
}

</style>