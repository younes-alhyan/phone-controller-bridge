const socket = new WebSocket(`ws://${location.host}/ws`);

const getGamepadButtons = (buttons) => {
  return buttons
    .filter((_, index) => index !== 6 && index !== 7)
    .map((button) => button.pressed);
};

const getGamepadTriggers = (triggers) => {
  return [
    {
      value: triggers[0].value,
      threshold: Number(document.getElementById(`threshold_left`).value),
    },
    {
      value: triggers[1].value,
      threshold: Number(document.getElementById(`threshold_right`).value),
    },
  ];
};

const getGamepadJoysticks = (joysticks) => {
  return [
    {
      x: {
        value: joysticks[0],
        invert: Number(document.getElementById(`inverted_left_x`).value),
      },
      y: {
        value: joysticks[1],
        invert: Number(document.getElementById(`inverted_left_y`).value),
      },
      dead_zone: Number(document.getElementById(`dead_zone_left`).value),
    },
    {
      x: {
        value: joysticks[2],
        invert: Number(document.getElementById(`inverted_right_x`).value),
      },
      y: {
        value: joysticks[3],
        invert: Number(document.getElementById(`inverted_right_y`).value),
      },
      dead_zone: Number(document.getElementById(`dead_zone_right`).value),
    },
  ];
};

const getGamepads = () => {
  return navigator
    .getGamepads()
    .filter((gamepad) => gamepad !== null)
    .map((gamepad) => ({
      id: gamepad.id,
      buttons: getGamepadButtons(gamepad.buttons),
      triggers: getGamepadTriggers([gamepad.buttons[6], gamepad.buttons[7]]),
      joysticks: getGamepadJoysticks(gamepad.axes),
    }));
};

const updateUI = (gamepads) => {
  const container = document.getElementById("gamepads");

  if (!gamepads.length) {
    container.innerHTML = `
          <div class="empty">
            No gamepads connected
          </div>
        `;
    return;
  }

  container.innerHTML = gamepads
    .map(
      (gamepad) => `
        <div class="gamepad">

          <h2>${escapeHTML(gamepad.id)}</h2>

          <div class="status">
            Connected
          </div>

          <h3>Buttons</h3>

          <div class="buttons">
            ${gamepad.buttons
              .map(
                (pressed, index) => `
              <div class="button ${pressed ? "pressed" : ""}">
                ${index}
              </div>
            `,
              )
              .join("")}
          </div>

          <h3>Triggers</h3>

          <div class="axes">
            ${gamepad.triggers
              .map(
                (trigger, index) => `
              <div class="axis">

                <div class="axis-name">
                  <span>
                    ${index === 0 ? "L2" : "R2"}
                  </span>

                  <span>
                    ${trigger.value.toFixed(2)}
                  </span>
                </div>

                <div class="axis-bar">
                  <div
                    class="axis-value"
                    style="width: ${trigger.value * 100}%"
                  ></div>
                </div>

              </div>
            `,
              )
              .join("")}
          </div>

          <h3>Joysticks</h3>

          <div class="axes">

            ${gamepad.joysticks
              .map(
                (joystick, index) => `
              <div class="axis">

                <div class="axis-name">
                  <span>
                    ${index === 0 ? "Left X" : "Right X"}
                  </span>

                  <span>
                    ${joystick.x.value.toFixed(2)}
                  </span>
                </div>

                <div class="axis-bar">
                  <div
                    class="axis-value"
                    style="
                      width: ${Math.abs(joystick.x.value) * 50}%;
                      margin-left: ${joystick.x.value < 0 ? 0 : 50}%;
                    "
                  ></div>
                </div>

              </div>

              <div class="axis">

                <div class="axis-name">
                  <span>
                    ${index === 0 ? "Left Y" : "Right Y"}
                  </span>

                  <span>
                    ${joystick.y.value.toFixed(2)}
                  </span>
                </div>

                <div class="axis-bar">
                  <div
                    class="axis-value"
                    style="
                      width: ${Math.abs(joystick.y.value) * 50}%;
                      margin-left: ${joystick.y.value < 0 ? 0 : 50}%;
                    "
                  ></div>
                </div>

              </div>
            `,
              )
              .join("")}

          </div>

        </div>
      `,
    )
    .join("");
};

const escapeHTML = (value) => {
  const div = document.createElement("div");
  div.textContent = value;
  return div.innerHTML;
};

const updateGamepads = () => {
  const gamepads = getGamepads();
  if (socket.readyState === WebSocket.OPEN) {
    socket.send(JSON.stringify(gamepads));
  }
  updateUI(gamepads);
  requestAnimationFrame(updateGamepads);
};

const rumbleHandler = (gamepad, strong, weak) => {
  if (!gamepad?.vibrationActuator) return;
  if (!strong && !weak) return gamepad.vibrationActuator.reset();
  gamepad.vibrationActuator.playEffect("dual-rumble", {
    duration: 5000,
    strongMagnitude: Number(strong),
    weakMagnitude: Number(weak),
  });
};

socket.onopen = () => updateGamepads();
socket.onmessage = (event) => {
  const data = JSON.parse(event.data);
  const { type, id } = data;
  const gamepad = navigator.getGamepads().find((gamepad) => gamepad?.id === id);
  if (type === "rumble") rumbleHandler(gamepad, data.strong, data.weak);
};
