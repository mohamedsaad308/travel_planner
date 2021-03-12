const trips = new Vue({
  components: {
    "create-trip": createTripComponent,
  },
  el: "#trips",
  delimiters: ["${", "}"],
  data: {
    trips: {},
    tripCount: null,
    error: "",
    showCreateTrip: false,
    ShowEditTrip: false,
    ShowDeleteTrip: false,
  },
  methods: {
    getTrips(pageNumber = 1) {
      this.page = pageNumber;
      fetch(`/api/trips?page=${pageNumber}`, {
        method: "GET",
        credentials: "include",
        cache: "no-cache",
        headers: new Headers({
          "content-type": "application/json",
        }),
      })
        .then((response) => response.json())
        .then((json) => {
          this.trips = json.trips;
          this.tripCount = json.count;
        });
    },
    createTripModal() {
      this.error = "";
      this.showCreateTrip = true;
    },
    addTrip(destination, startDate, endDate, comment) {
      if (!destination || !startDate || !endDate) {
        this.error = "You have to select destination, start date and end date";
      } else {
        fetch("/trips", {
          method: "POST",
          credentials: "include",
          cashe: "no-cashe",
          body: JSON.stringify({
            destination: destination,
            start_date: startDate,
            end_date: endDate,
            comment: comment,
          }),
          headers: new Headers({
            "content-type": "application/json",
          }),
        })
          .then((response) => response.json)
          .then((json) => console.log(json));
      }
    },
  },
  created() {
    this.getTrips();
  },
});
