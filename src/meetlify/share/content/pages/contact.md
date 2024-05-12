---
title: Contact Us
date:  2024-05-21
author:  Faisal Shahzad
slug:  contact
status: Draft
featureimage: lindau.png
description: Contact Us
---
<!-- Contact form-->
<div class="text-left mb-5">
    <h1 class="fw-bolder">Contact Us</h1>
    <p class="lead fw-normal text-muted mb-0">We'd love to hear from you</p>
</div>
<div class="row">
    <div class="col-lg-6">
        <form name="contact" method="POST" data-netlify="true">
            <!-- Name input-->
            <div class="form-floating mb-3">
                <input class="form-control" id="name" name="name" type="text" placeholder="Enter your name..."
                    data-sb-validations="required" />
                <label for="name">Full name</label>
                <div class="invalid-feedback" data-sb-feedback="name:required">A name is required.
                </div>
            </div>
            <!-- Email address input-->
            <div class="form-floating mb-3">
                <input class="form-control" id="email" name="email" type="email" placeholder="name@example.com"
                    data-sb-validations="required,email" />
                <label for="email">Email address</label>
                <div class="invalid-feedback" data-sb-feedback="email:required">An email is
                    required.</div>
                <div class="invalid-feedback" data-sb-feedback="email:email">Email is not valid.
                </div>
            </div>
            <!-- Message input-->
            <div class="form-floating mb-3">
                <textarea class="form-control" id="message" name="message" type="text"
                    placeholder="Enter your message here..." style="height: 10rem"
                    data-sb-validations="required"></textarea>
                <label for="message">Message</label>
                <div class="invalid-feedback" data-sb-feedback="message:required">A message is
                    required.
                </div>
            </div>
            <!-- Submit success message-->
            <div class="d-none" id="submitSuccessMessage">
                <div class="text-center mb-3">
                    <div class="fw-bolder">Thank You for Contacting us. We will get back to you soon!</div>
                </div>
            </div>
            <!-- Submit error message-->
            <div class="d-none" id="submitErrorMessage">
                <div class="text-center text-danger mb-3">Error sending message!. We did not recieve you message. Please try again.</div>
            </div>
            <!-- Submit Button-->
            <div class="d-grid"><button class="btn btn-primary btn-lg mb-5" id="submitButton"
                    type="submit">Submit</button>
            </div>
        </form>
    </div>
    <div class="col-lg-2">
    </div>
    <div class="col-lg-4">
        <!-- Contact cards-->
        <div class="gx-5">
            <div class="col">
                <div class="feature bg-primary bg-gradient text-white rounded-3 mb-3"><i
                        class="bi bi-chat-dots"></i>
                </div>
                <div class="h5 mb-2">Chat with us</div>
                <p class="text-muted mb-4">Visit us in one of our meetup for chit-chat.</p>
            </div>
            <div class="col">
                <div class="feature bg-primary bg-gradient text-white rounded-3 mb-3"><i
                        class="bi bi-people"></i></div>
                <div class="h5">Ask the community</div>
                <p class="text-muted mb-4">Join our community and explore best of Python</p>
            </div>
            <div class="col">
                <div class="feature bg-primary bg-gradient text-white rounded-3 mb-3"><i
                        class="bi bi-question-circle"></i>
                </div>
                <div class="h5">Projects</div>
                <p class="text-muted mb-4">Learn more about our GitHub projects.
                </p>
            </div>
        </div>
    </div>
</div>