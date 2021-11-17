function openPage(pageName, elmnt, color) {
	// Hide all elements with class="tabcontent" by default */
	var i, tabcontent, tablinks;
	tabcontent = document.getElementsByClassName("tabcontent");
	for (i = 0; i < tabcontent.length; i++) {
		tabcontent[i].style.display = "none";
	}
	// Remove the background color of all tablinks/buttons
	tablinks = document.getElementsByClassName("tablink");
	for (i = 0; i < tablinks.length; i++) {
		tablinks[i].style.backgroundColor = "";
	}
	// Show the specific tab content
	document.getElementById(pageName).style.display = "block";
	// Add the specific color to the button used to open the tab content
	elmnt.style.backgroundColor = color;
}
// Get the element with id="defaultOpen" and click on it
document.getElementById("defaultOpen").click();

const logout = async () => {
	const response = await fetch(URI + "logout");
	window.location.replace(URI + "login");
	//const myJson = await response.json();
};

const add = async () => {};

const populateEnrolled = async () => {
	const response = await fetch(URI + "student/data");
	const myJson = await response.json();

	for (let index = 0; index < myJson.length; index++) {
		const element = myJson[index];

		grades = element[0].grades;
		teacherName = element[1].teacher;
		courseName = element[2].class_name;
		stuEnrolled = element[3].enrolled + "/" + element[4].max_enrolled;
		classTime = element[5].time;

		globalCourses.newCourse(
			element[1].teacher,
			element[2].class_name,
			element[3].enrolled + "/" + element[4].max_enrolled,
			element[5].time,
			element[0].grades,
			1,
			element[3].enrolled == element[4].max_enrolled
		);

		$("#classEnrolled tr:last").after(
			"<tr><td>" +
				courseName +
				"</td><td>" +
				teacherName +
				"</td><td>" +
				classTime +
				"</td><td>" +
				stuEnrolled +
				"</td><td>" +
				grades +
				"</td></tr>"
		);
	}
};

const populateCourses = async () => {
	const response = await fetch(URI + "student/classes");
	const myJson = await response.json();

	for (let index = 0; index < myJson.length; index++) {
		const element = myJson[index];

		// console.log(element)

		//check if global student courses already contains ths if not add else skip
        if (element[2].enrolled == element[3].max_enrolled) {
            if (globalCourses.checkEnrolled(element[1].class_name)) {
                console.log(
                    globalCourses.newCourse(
                        element[0].teacher,
                        element[1].class_name,
                        element[2].enrolled + "/" + element[3].max_enrolled,
                        element[4].time,
                        -1,
                        0,
                        element[2].enrolled == element[3].max_enrolled
                    )
                );
                $("#addCourses tr:last").after(
                    "<tr><td>" +
                    element[1].class_name +
                    "</td><td>" +
                    element[0].teacher +
                    "</td><td>" +
                    element[4].time +
                    "</td><td>" +
                    element[2].enrolled +
                    "/" +
                    element[3].max_enrolled +
                    "</td><td>" +
                    "<button class='edit-button' onclick='add()'> delete </button>" +
                    "</td></tr>"
                );
            } else {
                $("#addCourses tr:last").after(
                    "<tr><td>" +
                    element[1].class_name +
                    "</td><td>" +
                    element[0].teacher +
                    "</td><td>" +
                    element[4].time +
                    "</td><td>" +
                    element[2].enrolled +
                    "/" +
                    element[3].max_enrolled +
                    "</td><td>" +
                    "<button class='edit-button' onclick='add()' disabled> full </button>" +
                    "</td></tr>"
                );
            }
        } else if (!globalCourses.checkEnrolled(element[1].class_name)) {
            $("#addCourses tr:last").after(
                "<tr><td>" +
                element[1].class_name +
                "</td><td>" +
                element[0].teacher +
                "</td><td>" +
                element[4].time +
                "</td><td>" +
                element[2].enrolled +
                "/" +
                element[3].max_enrolled +
                "</td><td>" +
                "<button class='edit-button' onclick='add()'  > add </button>" +
                "</td></tr>"
            );
        } else {
            $("#addCourses tr:last").after(
                "<tr><td>" +
                element[1].class_name +
                "</td><td>" +
                element[0].teacher +
                "</td><td>" +
                element[4].time +
                "</td><td>" +
                element[2].enrolled +
                "/" +
                element[3].max_enrolled +
                "</td><td>" +
                "<button class='edit-button' onclick='add()'> delete </button>" +
                "</td></tr>");
        }
	}
};

class Courses {
	constructor() {
		this.courses = [];
	}
	newCourse(
		teacherName,
		courseName,
		stuEnrolled,
		classTime,
		grades,
		enrolled,
		full
	) {
		let course = new Course(
			teacherName,
			courseName,
			stuEnrolled,
			classTime,
			grades,
			enrolled,
			full
		);
		this.courses.push(course);
		return course;
	}
	checkEnrolled(name) {
		for (let index = 0; index < this.courses.length; index++) {
			if (
				name == this.courses[index].courseName &&
				this.courses[index].full
			) {
				console.log(this.courses[index].full);
				return true;
			}
			if (
				name == this.courses[index].courseName &&
				this.courses[index].enrolled
			) {
				console.log(this.courses[index].enrolled);
				return true;
			}
		}
	}
}

class Course {
	constructor(
		teacherName,
		courseName,
		stuEnrolled,
		classTime,
		grades,
		enrolled,
		full
	) {
		this.teacherName = teacherName;
		this.courseName = courseName;
		this.stuEnrolled = stuEnrolled;
		this.classTime = classTime;
		this.grades = grades;
		this.enrolled = enrolled;
		this.full = full;
	}
}

const test = async () => {
	const response = await fetch(URI + "student/classes");
	const myJson = await response.json();

	console.log(myJson);
};

$(document).ready(function () {
	populateEnrolled();
	setTimeout(function () {
		populateCourses();
	}, 2000);
});

let globalCourses = new Courses();

URI = "http://127.0.0.1:5000/";
