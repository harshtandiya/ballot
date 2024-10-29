# Contributing

## Setting up the developer environment

* Ballot is built using the [frappe framework](https://frappeframework.com/docs/user/en/basics)
  and a basic understanding of it is necessary to contribute to the codebase
* [Install and setup frappe-bench](https://frappeframework.com/docs/user/en/tutorial/install-and-setup-bench).
  We recommend using [pipx](https://github.com/pypa/pipx) to install
  `frappe-bench` and updating the `PATH` variable to include the `.../bin/`
  folder inside the `pipx`-created Python virtual environment for `frappe-bench`
* Create a new bench with `bench init ballot`. We recommend storing benches
  in a single location e.g. `~/frappe-benches`
* CD into the bench directory i.e. `ballot` and clone the Ballot app using
  `bench get-app https://github.com/harshtandiya/ballot`. This will clone the
  Git repository into the `apps/` folder in the bench directory
* Create a [new site](https://frappeframework.com/docs/user/en/tutorial/create-a-site)
  using `bench new-site test.ballot`
* Install the Ballot app on the new site `bench --site test.ballot install-app ballot`
* [Access the site conveniently](https://frappeframework.com/docs/user/en/tutorial/create-a-site#access-site-in-your-browser)
  from your computer using `bench --site test.ballot add-to-hosts`
* Finally, run `bench start` to launch the backend

The frappe framework-powered backend application should now be running. To run
the Vue.js-powered frontend application, run `yarn dev` from the root
directory.

The website can now be accessed from `http://test.ballot:8080` and the backend
frappe app can be accessed from `http://test.ballot:<port number>`.
