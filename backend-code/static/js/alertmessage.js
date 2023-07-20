// const app = new Vue ({
//   el: '#app',
//   delimiters: ['${', '}'],
//   data:{
//       count: 0,
//       alertMessage: ''
//   },
//   methods: {
//     showAlert() {
//       this.alertMessage = 'This is an alert message.';
//     },
//     dismissAlert() {
//       this.alertMessage = '';
//     }
//   }
// });
const app = new Vue({
  el: '#app',
  delimiters: ['${', '}'],
  data:{
      alertMessage: ''
  },
  methods: {
    dismissAlert() {
      this.alertMessage = '';
    }
  },
  mounted: function() {
    source = new EventSource("/stream");
    source.addEventListener('greeting', event => {
        this.alertMessage = 'This is an alert message.';
    }, false);
  } 
});

