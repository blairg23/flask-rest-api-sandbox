function UsersViewModel() {
	var self = this;
	self.usersURI = '/userlist/api/v1.0/users';
	self.username = "";
	self.password = "";
	self.users = ko.observableArray();

	self.ajax = function(uri, method, data) {
		var request = {
			url: uri,
			type: method,
			contentType: "application/json",
			accepts: "application/json",
			cache: false,
			dataType: 'json',
			data: JSON.stringify(data),
			beforeSend: function (xhr) {
				xhr.setRequestHeader("Authorization", 
					"Basic " + btoa(self.username + ":" + self.password));
			},
			error: function(jqXHR) {
				console.log("ajax error " + jqXHR.status);
			}
		};		
		return $.ajax(request);
	}
	self.updateUser = function(user, newUser) {
		var i = self.users.indexOf(user);
		self.users()[i].first_name(newUser.first_name);
		self.users()[i].last_name(newUser.last_name);
		self.users()[i].birthdate(newUser.birthdate);
		self.users()[i].zip_code(newUser.zip_code);
	}

	self.beginAdd = function() {
		$('#add').modal('show');
	}
	self.add = function(user) {
		self.ajax(self.usersURI, 'POST', user).done(function(data) {
			self.users.push({
				first_name: ko.observable(data.user.first_name),
				last_name: ko.observable(data.user.last_name),
				birthdate: ko.observable(data.user.birthdate),
				zip_code: ko.observable(data.user.zip_code),
				uri: ko.observable(data.user.uri)
			});
		});
	}
	self.beginEdit = function(user) {
		EditUserViewModel.setUser(user);
		$('#edit').modal('show');
	}
	self.edit = function(user, data) {
		self.ajax(user.uri(), 'PUT', data).done(function(res) {
			self.updateUser(user, res.user);
		});
	}
	self.remove = function(user) {
		self.ajax(user.uri(), 'DELETE').done(function() {
			self.users.remove(user);
		});
	}
	self.beginLogin = function() {
		$('#login').modal('show');
	}
	self.login = function(username, password) {
		self.username = username;
		self.password = password;
		self.ajax(self.usersURI, 'GET').done(function(data) {
			for (var i = 0; i < data.users.length; i++) {
				self.users.push({
					first_name: ko.observable(data.users[i].first_name),
					last_name: ko.observable(data.users[i].last_name),
					birthdate: ko.observable(data.users[i].birthdate),
					zip_code: ko.observable(data.users[i].zip_code),
					uri: ko.observable(data.users[i].uri)
				});
			}
		}).fail(function(jqXHR) {
			if (jqXHR.status == 403)
				setTimeout(self.beginLogin, 500);
		});
	}
	
	self.beginLogin();
}
function AddUserViewModel() {
	var self = this;
	self.first_name = ko.observable();
	self.last_name = ko.observable();
	self.birthdate = ko.observable();
	self.zip_code = ko.observable();
	self.uri = ko.observable();

	self.addUser = function() {
		$('#add').modal('hide');
		UsersViewModel.add({
			first_name: self.first_name(),
			last_name: self.last_name(),
			birthdate: self.birthdate(),
			zip_code: self.zip_code(),
			uri: self.uri()
		});
		self.first_name("");
		self.last_name("");
		self.birthdate("");
		self.zip_code("");
		self.uri("");
	}
}
function EditUserViewModel() {
	var self = this;
	self.first_name = ko.observable();
	self.last_name = ko.observable();
	self.birthdate = ko.observable();
	self.zip_code = ko.observable();
	self.uri = ko.observable();

	self.setUser = function(user) {
		self.user = user;
		self.first_name(user.first_name());
		self.last_name(user.last_name());
		self.birthdate(user.birthdate());
		self.zip_code(user.zip_code());
		
		$('edit').modal('show');
	}

	self.editUser = function() {
		$('#edit').modal('hide');
		UsersViewModel.edit(self.user, {
			first_name: self.first_name(),
			last_name: self.last_name(),
			birthdate: self.birthdate(),
			zip_code: self.zip_code(),
		});
	}
}
function LoginViewModel() {
	var self = this;
	self.username = ko.observable();
	self.password = ko.observable();

	self.login = function() {
		$('#login').modal('hide');
		UsersViewModel.login(self.username(), self.password());
	}
}

ko.bindingHandlers.masked = {
	init: function(element, valueAccessor, allBindingsAccessor) {
		var mask = allBindingsAccessor().mask || {};
		$(element).mask(mask);
		ko.utils.registerEventHandler(element, 'focusout', function() {
			var observable = valueAccessor();
			observable($(element).val());
		});
	}, 
	update: function (element, valueAccessor) {
		var value = ko.utils.unwrapObservable(valueAccessor());
		$(element).val(value);
	}
};
