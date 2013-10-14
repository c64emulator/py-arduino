var pyArduinoModule = angular.module('PyArduino', [ 'uiSlider' ]);

// pyArduinoModule.factory('pyArduinoHttpClient', [ '$http', function($http) {
// var get_arduino_data_url = '/angular/get_arduino_data/';
// return {
// get_arduino_data : function() {
// return $http.get(get_arduino_data_url);
// }
// };
// } ]);

pyArduinoModule.controller('GlobalController', function($scope) {

    $scope.CONST = {
        INPUT : 0,
        OUTPUT : 1
    };

    $scope.avr_cpu_type = '(unknown)';
    $scope.arduino_type = {};
    $scope.enhanced_arduino_type = {};

});

pyArduinoModule.controller('PinsController', function($scope, $http) {

    var get_arduino_data_url = '/angular/get_arduino_data/';
    var digital_pin_mode_url = '/angular/digital_pin_mode/';

    var MODE_PIN_DISABLED= -1; // FIXME: this doesn't exists in py-arduino!
    var INPUT = 0;
    var OUTPUT = 1;
    var CSS_FOR_SELECTED_MODE = 'btn-success';
    var CSS_FOR_NON_SELECTED_MODE = 'btn-default';

    $scope.editMode = false;

    $scope.editModeEnter = function() {
        $scope.editMode = true;
    };

    $scope.editModeExit = function() {
        $scope.editMode = false;
        // TODO: save changes!
    };

    $scope.pinModeDisabled = function(pinStruct) {
        $scope.setDigitalPinMode(pinStruct.pin, MODE_PIN_DISABLED);
        // $scope.refreshCssForButtons();
    };

    $scope.pinModeInput = function(pinStruct) {
        $scope.setDigitalPinMode(pinStruct.pin, INPUT);
        // $scope.refreshCssForButtons();
    };

    $scope.pinModeOutput = function(pinStruct) {
        $scope.setDigitalPinMode(pinStruct.pin, OUTPUT);
        // $scope.refreshCssForButtons();
    };

    $scope.refreshCssForButtons = function() {
        for (i = 0; i < $scope.enhanced_arduino_type.digital_pins_struct.length; i++) {
            var pin_struct = $scope.enhanced_arduino_type.digital_pins_struct[i];
            // console.debug("pin_struct[" + i + "].status_mode_is_input: " +
            // pin_struct.status_mode_is_input)
            // console.debug("pin_struct[" + i + "].status_mode_is_output: " +
            // pin_struct.status_mode_is_output)
            if (pin_struct.status_mode_is_input) {
                pin_struct.css_for_button_unknown_mode = CSS_FOR_NON_SELECTED_MODE;
                pin_struct.css_for_button_input_mode = CSS_FOR_SELECTED_MODE;
                pin_struct.css_for_button_output_mode = CSS_FOR_NON_SELECTED_MODE;
            } else if (pin_struct.status_mode_is_output) {
                pin_struct.css_for_button_unknown_mode = CSS_FOR_NON_SELECTED_MODE;
                pin_struct.css_for_button_input_mode = CSS_FOR_NON_SELECTED_MODE;
                pin_struct.css_for_button_output_mode = CSS_FOR_SELECTED_MODE;
            } else {
                pin_struct.css_for_button_unknown_mode = CSS_FOR_SELECTED_MODE;
                pin_struct.css_for_button_input_mode = CSS_FOR_NON_SELECTED_MODE;
                pin_struct.css_for_button_output_mode = CSS_FOR_NON_SELECTED_MODE;
            }
        }

        for (i = 0; i < $scope.enhanced_arduino_type.analog_pins_struct.length; i++) {
            var pin_struct = $scope.enhanced_arduino_type.analog_pins_struct[i];
            // console.debug("pin_struct[" + i + "].status_mode_is_input: " +
            // pin_struct.status_mode_is_input)
            if (pin_struct.status_mode_is_input) {
                pin_struct.css_for_button_unknown_mode = CSS_FOR_NON_SELECTED_MODE;
                pin_struct.css_for_button_input_mode = CSS_FOR_SELECTED_MODE;
                pin_struct.css_for_button_output_mode = CSS_FOR_NON_SELECTED_MODE;
            } else {
                pin_struct.css_for_button_unknown_mode = CSS_FOR_SELECTED_MODE;
                pin_struct.css_for_button_input_mode = CSS_FOR_NON_SELECTED_MODE;
                pin_struct.css_for_button_output_mode = CSS_FOR_NON_SELECTED_MODE;
            }
        }

    };

    $scope.refreshPinInfo = function() {
        console.info("refreshPinInfo()");
        $http.get(get_arduino_data_url).success(function(data) {

            console.debug("$http.get() -> success -> " + data);
            $scope.avr_cpu_type = data.avr_cpu_type;
            $scope.arduino_type = data.arduino_type;
            $scope.enhanced_arduino_type = data.enhanced_arduino_type;

            console.debug("$scope.avr_cpu_type: " + $scope.avr_cpu_type);
            console.debug("$scope.arduino_type: " + $scope.arduino_type);
            console.debug("$scope.enhanced_arduino_type: " + $scope.enhanced_arduino_type);
            console.debug("$scope.enhanced_arduino_type.digital_pins_struct: " + $scope.enhanced_arduino_type.digital_pins_struct);

            var i;

            // Digitales...
            $scope.refreshCssForButtons();

            // "enhanced_arduino_type": {
            // "digital_pins_struct": [
            // .... {
            // .... .... "pwm": false,
            // .... .... "enabled_in_web": true,
            // .... .... "pin": 0,
            // .... .... "pin_id": null,
            // .... .... "status_written_value": null,
            // .... .... "status_read_value": null,
            // .... .... "status_mode": null,
            // .... .... "status_mode_is_input": true|false,
            // .... .... "status_mode_is_output": true|false,
            // .... .... "status_mode_is_unknown": true|false,
            // .... .... "digital": true,
            // .... .... "pk": 1,
            // .... .... "label": "Digital pin #0"
            // .... },
            // ],
            // "analog_pins_struct": [
            // .... {
            // .... .... "pwm": false,
            // .... .... "enabled_in_web": true,
            // .... .... "pin": 0,
            // .... .... "pin_id": null,
            // .... .... "status_written_value": null,
            // .... .... "status_read_value": null,
            // .... .... "status_mode": null,
            // .... .... "status_mode_is_input": true|false,
            // .... .... "status_mode_is_unknown": true|false,
            // .... .... "digital": true,
            // .... .... "pk": 55,
            // .... .... "label": "Analog pin #0"
            // .... },
            // ],

        }).error(function(data) {
            console.error("refreshPinInfo() -> $http.get() -> ERROR -> " + data);
        });
    };

    $scope.setDigitalPinMode = function(pin, mode) {

        console.info("setPinMode()");
        $http.post(digital_pin_mode_url, {
            pin : pin,
            mode : mode
        }).success(function(data) {

            console.info("setPinMode() OK! :-D");

            $scope.avr_cpu_type = data.avr_cpu_type;
            $scope.arduino_type = data.arduino_type;
            $scope.enhanced_arduino_type = data.enhanced_arduino_type;
            $scope.refreshCssForButtons();

        }).error(function(data) {
            console.error("setPinMode() -> $http.post() -> ERROR -> " + data);
        });

    };

});
