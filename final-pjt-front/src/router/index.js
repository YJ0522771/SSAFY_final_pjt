import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '@/views/Home'
import Signup from '@/views/accounts/Signup'
import Login from '@/views/accounts/Login'
import Profile from '@/views/accounts/Profile'
import MovieList from '@/views/movies/MovieList'
import MovieRandomList from '@/views/movies/MovieRandomList'
import MoviePlayingList from '@/views/movies/MoviePlayingList'
import MovieGenreList from '@/views/movies/MovieGenreList'
import MovieRecommend from '@/views/movies/MovieRecommend'
import MovieDetail from '@/views/movies/MovieDetail'
// import MovieInfo from '@/views/movies/MovieInfo'
import ReviewList from '@/views/community/ReviewList'
import ReviewCreate from '@/views/community/ReviewCreate'
import ReviewDetail from '@/views/community/ReviewDetail'
import ReviewRevise from '@/views/community/ReviewRevise'

// import VueFilterDateFormat from 'vue-filter-date-format';

// Vue.use(VueFilterDateFormat)
import "moment/locale/ko"
import moment from 'moment'

Vue.filter('dateFilter', function(value) {
  if (value) {
    // return moment(String(value)).format('MM/DD/YYYY hh:mm')
    // return moment(String(value)).format('MMMM Do YYYY, h:mm:ss a')
    return moment(String(value)).from(new Date())
  }
})

Vue.use(VueRouter)

const originalPush = VueRouter.prototype.push;
VueRouter.prototype.push = function push(location) {
	return originalPush.call(this, location).catch(err => {
		if (err.name !== 'NavigationDuplicated') throw err;
	});
};

const routes = [
  {
    path: '/home',
    name: 'Home',
    component: Home,
  },
  {
    path: '/movies',
    name: 'MovieList',
    component: MovieList,
    children: [
      {
        name: 'MovieRandomList',
        path: 'random',
        component: MovieRandomList
      },
      {
        name: 'MoviePlayingList',
        path: 'playing',
        component: MoviePlayingList
      },
      {
        name: 'MovieGenreList',
        path: 'genre',
        component: MovieGenreList
      },
    ]
  },
  {
    path: '/movies/recommend',
    name: 'MovieRecommend',
    component: MovieRecommend,
  },
  {
    path: '/movies/:id',
    name: 'MovieDetail',
    component: MovieDetail,
  },
  {
    path: '/community/:id',
    name: 'ReviewList',
    component: ReviewList,
    children: []
  },
  {
    path: '/create',
    name: 'ReviewCreate',
    component: ReviewCreate
  },
  {
    path: '/detail/:review_id',
    name: 'ReviewDetail',
    component: ReviewDetail
  },
  {
    path: '/:review_id/detail/put',
    name: 'ReviewRevise',
    component: ReviewRevise
  },
  {
    path: '/accounts/signup',
    name: 'Signup',
    component: Signup,
  },
  {
    path: '/accounts/login',
    name: 'Login',
    component: Login,
  },
  {
    path: '/accounts/Profile/:username',
    name: 'Profile',
    component: Profile,
  },
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
