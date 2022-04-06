<template>
  <!-- <div>
    <span
    @click="goReviewDetail">{{ review.title }}</span> | 
    <span>{{ review.vote }}</span> |
    <span>{{ review.username }}</span>
  </div> -->

  <tbody>
    <tr class="reviews"
    @click="goReviewDetail">
      <td>{{ review.id }}</td>
      <td>
      <p class="text-decoration-none fw-bold"
      >{{ review.title }}</p>
      </td>
      <td class="fw-bold">{{ review.vote }}</td>
      <td>{{ review.username }}</td>
      <td>{{ review.created_at | dateFilter}}</td>
    </tr>
  </tbody>
</template>

<script>
export default {
  name: 'Review',
  props: {
    review: Object,
  },
  methods: {
    goReviewDetail: function () {
      this.$emit('review-detail', this.review.id)
    }
  }
}
</script>

<style>
.review-table p {
  font-size: 18px;
  padding-bottom: 0;
  margin-bottom: 0;
}

.reviews:hover {
  background-color: rgba(255, 254, 254, 0.582);
  cursor: pointer;
}
</style>