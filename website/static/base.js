const appData = () => {
  // set initial value of percent to 0
  return {
    percent: 0,

    // function to initialize app and add scroll event listener
    appInit() {
      window.addEventListener("scroll", () => {
        let winScroll =
            document.body.scrollTop || document.documentElement.scrollTop,
          height =
            document.documentElement.scrollHeight -
            document.documentElement.clientHeight;

        // calculate scroll percentage and round to nearest integer
        this.percent = Math.round((winScroll / height) * 100);
      });
    },
  };
};
