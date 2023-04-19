console.log("Iam working");
const appData = () => {
    return {
        percent: 0,

        appInit() {
            window.addEventListener('scroll', () => {
                let winScroll = document.body.scrollTop || document.documentElement.scrollTop,
                    height = document.documentElement.scrollHeight - document.documentElement.clientHeight;

                this.percent = Math.round((winScroll / height) * 100);
            });
        },
    };
};