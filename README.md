# icsMiddleman

(c) 2018 J. W. Crockett, Jr.<sup><a href="#footnote1">1</a></sup>, [@joshcvt](http://twitter.com/joshcvt)

**icsMiddleman** is a lightweight Python 2.7 [Chalice](https://github.com/aws/chalice) service to sit between your .ICS-consuming calendaring solution (GCal, Calendar.app, etc) and regularly updated public ICS calendars you'd like to consume in a munged form.  The initial target build is Minor League Baseball, which in 2018 abandoned its prior willingness to syndicate schedules to Google Calendar in favor of a deal with a third party who stuffs the calendar full of boilerplate and tries to hide the ICS URL, instead telling you to grant it access to your Google account to get that data.  But looking at the code should make it fairly obvious how you can generalize it to your own obnoxious actor.

Not yet usable.

----
<a name="footnote1"/><sup>1</sup> The developer of this application claims no rights to or control over the data sources it targets or the data contained within. Users of this application are themselves solely responsible for assuring that their use of this application, the sources and the data contained within complies with any and all terms and conditions set by the owners of the data sources.