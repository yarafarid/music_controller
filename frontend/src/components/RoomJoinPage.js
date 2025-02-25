import React, { useState } from "react";
import { TextField, Button, Typography } from "@mui/material";
import Grid from "@material-ui/core/Grid";
import { Link, useNavigate } from "react-router-dom";
const RoomJoinPage = () => {
  const [roomCode, setRoomCode] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();
  const handleTextFieldChange = (e) => {
    setRoomCode(e.target.value);
  };
  const handleRoomButtonPressed = () => {
    // send a post request to the backend to join a room
    const requestOptions = {
      method: "POST",
      headers: {"Content-type": "application/json"},
      body: JSON.stringify({ code: roomCode }),
    };
    fetch("/api/join-room", requestOptions)
      .then((response) => {
        if (response.ok) {
          navigate("/room/" + roomCode);
        } else {
          return response.json().then((data) => {
            setError(data.message || "Room not found.");
          });
        }
      })
      .catch((error) => {
        console.error("Error:", error);
        setError("An error occurred while trying to join the room.");
      });
  };
  return (
    <Grid container spacing={1}>
      <Grid item xs={12} align="center">
        <Typography component="h4" variant="h4">
          Join A Room
        </Typography>
      </Grid>
      <Grid item xs={12} align="center">
        <TextField
          error={error}
          label="Code"
          placeholder="Enter a Room Code"
          value={roomCode}
          helperText={error}
          variant="outlined"
          onChange={handleTextFieldChange}
        />
      </Grid>
      <Grid item xs={12} align="center">
        <Button
          variant="contained"
          color="primary"
          component={Link}
          onClick={handleRoomButtonPressed}
        >
          Enter Room
        </Button>
      </Grid>
      <Grid item xs={12} align="center">
        <Button variant="contained" color="secondary" to="/" component={Link}>
          Back
        </Button>
      </Grid>
    </Grid>
  );
};
export default RoomJoinPage;
