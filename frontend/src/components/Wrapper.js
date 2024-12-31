/**
 * ==========================================================
 *  Stackpay Wrapper Component
 * ----------------------------------------------------------
 *  This file contains the Wrapper component for the
 *  Stackpay React application, serving as a layout component
 *  that includes the navigation bar and sidebar.
 *
 *  Project: Stackpay
 *  Developed with: FastAPI, Redis, React
 *  Author: idarbandi
 *  Contact: darbandidr99@gmail.com
 *  GitHub: https://github.com/idarbandi
 * ==========================================================
 */

/**
 * Wrapper Component
 *
 * This component serves as the layout component, including the
 * navigation bar, sidebar, and main content area.
 */

export const Wrapper = (props) => {
  return (
    <>
      <header className="navbar navbar-dark sticky-top bg-dark flex-md-nowrap p-0 shadow stack-navbar">
        <a className="navbar-brand col-md-3 col-lg-2 me-0 px-3 stack-navbar-brand" href="#">
          Stackpay
        </a>

        <div className="navbar-nav">
          <div className="nav-item text-nowrap">
            <a className="nav-link px-3 stack-signout-link" href="#">
              Sign out
            </a>
          </div>
        </div>
      </header>

      <div className="container-fluid stack-container">
        <div className="row">
          <nav id="sidebarMenu" className="col-md-3 col-lg-2 d-md-block bg-light sidebar collapse stack-sidebar">
            <div className="position-sticky pt-3">
              <ul className="nav flex-column">
                <li className="nav-item">
                  <a className="nav-link active stack-nav-link" aria-current="page" href="#">
                    Products
                  </a>
                </li>
              </ul>
            </div>
          </nav>

          <main className="col-md-9 ms-sm-auto col-lg-10 px-md-4 stack-main">{props.children}</main>
        </div>
      </div>
    </>
  );
};
