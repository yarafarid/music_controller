import React, { useState } from "react";
import Grid from "@material-ui/core/Grid";
import Typography from "@mui/material/Typography";
import FormHelperText from "@mui/material/FormHelperText";
import FormControl from "@mui/material/FormControl";
import Radio from "@mui/material/Radio";
import RadioGroup from "@mui/material/RadioGroup";
import FormControlLabel from "@mui/material/FormControlLabel";
import Button from "@mui/material/Button";
import TextField from "@mui/material/TextField";
import { Form, Link, useNavigate } from "react-router-dom";
import { Collapse } from "@mui/material";
import Alert from "@mui/material/Alert";
const CreateRoomPage = ({
  update: initialUpdate = false,
  votesToSkip: initialVotesToSkip = 2,
  guestCanPause: initialGuestCanPause = true,
  updateCallback = () => {},
  roomCode,
}) => {
  const [guestCanPause, setGuestCanPause] = useState(initialGuestCanPause);
  const [votesToSkip, setVotesToSkip] = useState(initialVotesToSkip);
  const [errorMsg, setErrorMsg] = useState("");
  const [successMsg, setSuccessMsg] = useState("");
  const navigate = useNavigate();

  const handleVotesChange = (e) => {
    setVotesToSkip(e.target.value);
  };
  const handleGuestCanPauseChange = (e) => {
    setGuestCanPause(e.target.value === "true" ? true : false);
  };
  const handleRoomButtonPressed = () => {
    // We need to send a request to the backend to create a room with the state
    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" }, // This is used to tell the backend that the data is in JSON format
      body: JSON.stringify({
        votes_to_skip: votesToSkip, // The name of the variable should be the same as the one in the backend
        guest_can_pause: guestCanPause, // The name of the variable should be the same as the one in the backend
      }),
    };
    fetch("/api/create-room", requestOptions) // send the request with the requestOptions to the backend
      .then((response) => response.json()) //once we get a response from the backend we convert it to JSON
      .then((data) => navigate("/room/" + data.code)); // Once we get the data we redirect the user to the room page with the room code
  };
  const handleUpdateButtonPressed = () => {
    const requestOptions = {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        votes_to_skip: votesToSkip,
        guest_can_pause: guestCanPause,
        code: roomCode, // the room code will be send to the backend because the backend will search in the data by the room code to catch the required room from database and update its settings
      }),
    };
    fetch("/api/update-room", requestOptions).then((response) => {
      if (response.ok) {
        updateCallback();
        setSuccessMsg("Room updated successfully!");
      } else {
        setErrorMsg("Error updating room...");
      }
    });
  };
  const title = initialUpdate == true ? "Update Room" : "Create A Room";
  const renderCreateButton = () => {
    return (
      <Grid container spacing={1}>
        <Grid item xs={12} align="center">
          <Button
            color="primary"
            variant="contained"
            onClick={handleRoomButtonPressed}
          >
            Create
          </Button>
        </Grid>
        <Grid item xs={12} align="center">
          <Button color="secondary" variant="contained" to="/" component={Link}>
            Back
          </Button>
        </Grid>
      </Grid>
    );
  };
  const renderUpdateButtons = () => {
    return (
      <Grid item xs={12} align="center">
        <Button
          color="primary"
          variant="contained"
          onClick={handleUpdateButtonPressed}
        >
          Update
        </Button>
      </Grid>
    );
  };
  return (
    <Grid container spacing={1}>
      <Grid item xs={12} align="center">
        <Collapse in={errorMsg != "" || successMsg != ""}>
          {successMsg != "" ? (
            <Alert
              severity="success"
              onClose={() => {
                setSuccessMsg("");
              }}
            >
              {successMsg}
            </Alert>
          ) : (
            <Alert
              severity="error"
              onClose={() => {
                setErrorMsg("");
              }}
            >
              {errorMsg}
            </Alert>
          )}
        </Collapse>
      </Grid>
      <Grid item xs={12} align="center">
        <Typography component="h4" variant="h4">
          {title}
        </Typography>
      </Grid>
      <Grid item xs={12} align="center">
        <FormControl component="fieldset">
          <FormHelperText>
            <div align="center">Guest Control of Playback State</div>
          </FormHelperText>
          <RadioGroup
            row
            defaultValue={guestCanPause.toString()}
            onChange={handleGuestCanPauseChange}
          >
            <FormControlLabel
              value="true"
              control={<Radio color="primary" />}
              label="Play/Pause"
              labelPlacement="bottom"
            />
            <FormControlLabel
              value="false"
              control={<Radio color="secondary" />}
              label="No Control"
              labelPlacement="bottom"
            />
          </RadioGroup>
        </FormControl>
      </Grid>
      <Grid item xs={12} align="center">
        <FormControl>
          <TextField
            required={true}
            type="number"
            defaultValue={votesToSkip}
            inputProps={{
              min: 1,
              style: { textAlign: "center" },
            }}
            onChange={handleVotesChange}
          />
          <FormHelperText>
            <div align="center">Votes Required to Skip Song</div>
          </FormHelperText>
        </FormControl>
      </Grid>
      {initialUpdate == true ? renderUpdateButtons() : renderCreateButton()}
    </Grid>
  );
};
export default CreateRoomPage;
