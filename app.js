async function api(url, options = {}) {

    const response = await fetch(
        url,
        {
            credentials: "include",
            ...options
        }
    );

    const data =
        await response
            .json()
            .catch(() => ({
                detail: "Server error"
            }));

    if (!response.ok) {

        throw new Error(
            data.detail || "Request failed"
        );
    }

    return data;
}


function showResults(data) {

    const root =
        document.getElementById(
            "results"
        );

    if (!root) {
        return;
    }

    root.innerHTML = `

        <section class="result">

            <h2>
                ${data.summary}
            </h2>

            <p>
                Budget:
                ₹${Number(
                    data.budget
                ).toLocaleString()}

                · Planned:
                ₹${Number(
                    data.budget_used
                ).toLocaleString()}

                · ${data.source}
            </p>

            ${
                data.recommendations
                    .map(item => `

                    <article
                        class="result-card"
                    >

                        <h3>
                            ${item.title}
                        </h3>

                        <p>
                            ${item.reason}
                        </p>

                        <p>

                            <b>
                                ₹${Number(
                                    item.estimated_price
                                ).toLocaleString()}
                            </b>

                            · ${item.category}

                            · ${item.platform}

                        </p>

                        <a
                            target="_blank"
                            rel="noopener"
                            href="${item.url}"
                        >
                            Search on
                            ${item.platform}
                        </a>

                    </article>

                `)
                .join("")
            }

        </section>
    `;
}


document.addEventListener(
    "DOMContentLoaded",
    () => {


        const loginForm =
            document.getElementById(
                "loginForm"
            );


        if (loginForm) {

            loginForm.onsubmit =
                async event => {

                    event.preventDefault();

                    try {

                        await api(
                            "/api/auth/login",
                            {

                                method: "POST",

                                headers: {
                                    "Content-Type":
                                        "application/json"
                                },

                                body:
                                    JSON.stringify(
                                        Object.fromEntries(
                                            new FormData(
                                                loginForm
                                            )
                                        )
                                    )
                            }
                        );

                        location =
                            "/dashboard";

                    } catch (error) {

                        document
                            .getElementById(
                                "message"
                            )
                            .textContent =
                            error.message;
                    }
                };
        }


        const registerForm =
            document.getElementById(
                "registerForm"
            );


        if (registerForm) {

            registerForm.onsubmit =
                async event => {

                    event.preventDefault();

                    try {

                        await api(
                            "/api/auth/register",
                            {

                                method: "POST",

                                headers: {
                                    "Content-Type":
                                        "application/json"
                                },

                                body:
                                    JSON.stringify(
                                        Object.fromEntries(
                                            new FormData(
                                                registerForm
                                            )
                                        )
                                    )
                            }
                        );

                        location =
                            "/dashboard";

                    } catch (error) {

                        document
                            .getElementById(
                                "message"
                            )
                            .textContent =
                            error.message;
                    }
                };
        }


        const homeForm =
            document.getElementById(
                "homeForm"
            );


        if (homeForm) {

            homeForm.onsubmit =
                async event => {

                    event.preventDefault();

                    try {

                        const data =
                            Object.fromEntries(
                                new FormData(
                                    homeForm
                                )
                            );

                        data.items =
                            data.items
                                ? JSON.parse(
                                    data.items
                                )
                                : {};

                        const result =
                            await api(
                                "/api/generate-home",
                                {

                                    method: "POST",

                                    headers: {
                                        "Content-Type":
                                            "application/json"
                                    },

                                    body:
                                        JSON.stringify(
                                            data
                                        )
                                }
                            );

                        showResults(
                            result
                        );

                    } catch (error) {

                        document
                            .getElementById(
                                "results"
                            )
                            .innerHTML =
                            `<p class="error">
                                ${error.message}
                            </p>`;
                    }
                };
        }


        const partyForm =
            document.getElementById(
                "partyForm"
            );


        if (partyForm) {

            partyForm.onsubmit =
                async event => {

                    event.preventDefault();

                    try {

                        const result =
                            await api(
                                "/api/generate-party",
                                {

                                    method: "POST",

                                    headers: {
                                        "Content-Type":
                                            "application/json"
                                    },

                                    body:
                                        JSON.stringify(
                                            Object.fromEntries(
                                                new FormData(
                                                    partyForm
                                                )
                                            )
                                        )
                                }
                            );

                        showResults(
                            result
                        );

                    } catch (error) {

                        document
                            .getElementById(
                                "results"
                            )
                            .innerHTML =
                            `<p class="error">
                                ${error.message}
                            </p>`;
                    }
                };
        }


        const jewelryForm =
            document.getElementById(
                "jewelryForm"
            );


        if (jewelryForm) {

            jewelryForm.onsubmit =
                async event => {

                    event.preventDefault();

                    try {

                        const result =
                            await api(
                                "/api/generate-jewelry",
                                {

                                    method: "POST",

                                    body:
                                        new FormData(
                                            jewelryForm
                                        )
                                }
                            );

                        showResults(
                            result
                        );

                    } catch (error) {

                        document
                            .getElementById(
                                "results"
                            )
                            .innerHTML =
                            `<p class="error">
                                ${error.message}
                            </p>`;
                    }
                };
        }


        const welcome =
            document.getElementById(
                "welcome"
            );


        if (welcome) {

            api(
                "/api/auth/session-info"
            )

                .then(data => {

                    welcome.textContent =
                        "Hello, " +
                        data.name +
                        ". Choose a planner.";

                })

                .catch(() => {

                    location =
                        "/login";
                });


            api(
                "/api/history"
            )

                .then(data => {

                    const recent =
                        document.getElementById(
                            "recent"
                        );

                    recent.innerHTML =
                        data
                            .slice(0, 5)
                            .map(
                                item =>
                                    `<p>
                                        ${item.planner}
                                        · ₹${Number(
                                            item.budget
                                        ).toLocaleString()}
                                    </p>`
                            )
                            .join("")
                        ||
                        "<p>No plans yet.</p>";
                });
        }


        const history =
            document.getElementById(
                "history"
            );


        if (history) {

            api(
                "/api/history"
            )

                .then(data => {

                    history.innerHTML =
                        data
                            .map(
                                item => `

                                <article
                                    class="result-card"
                                >

                                    <h3>
                                        ${item.planner.toUpperCase()}
                                        PLAN
                                    </h3>

                                    <p>
                                        ₹${Number(
                                            item.budget
                                        ).toLocaleString()}

                                        ·

                                        ${new Date(
                                            item.created_at
                                        ).toLocaleString()}
                                    </p>

                                    <p>
                                        ${item.result.summary}
                                    </p>

                                </article>

                            `
                            )
                            .join("")
                        ||
                        "<p>No history.</p>";

                })

                .catch(() => {

                    location =
                        "/login";
                });
        }

    }
);