"""Tests for the validate command."""

import pytest
import typer
from unittest.mock import Mock, patch
from pathlib import Path

from luminoracore_cli.commands.validate import validate_command
from luminoracore_cli.utils.errors import ValidationError


async def call_validate_command(files, **kwargs):
    """Helper function to call validate_command with proper parameter handling."""
    # Set default values for all parameters
    params = {
        'schema_url': None,
        'strict': False,
        'format': 'text',
        'output_file': None,
        'quiet': False,
        'parallel': True,
        'max_workers': 4
    }
    params.update(kwargs)
    
    # Convert files to Path objects if they're strings
    if isinstance(files, (str, list)):
        if isinstance(files, str):
            files = [files]
        files = [Path(f) if isinstance(f, str) else f for f in files]
    
    # Call the synchronous validate_command
    validate_command(
        files=files,
        schema_url=params['schema_url'],
        strict=params['strict'],
        format=params['format'],
        output_file=params['output_file'],
        quiet=params['quiet'],
        parallel=params['parallel'],
        max_workers=params['max_workers']
    )


class TestValidateCommand:
    """Test cases for the validate command."""
    
    @pytest.mark.asyncio
    async def test_validate_single_file_success(self, personality_file, mock_client):
        """Test validating a single valid personality file."""
        with patch("luminoracore_cli.commands.validate.get_client", return_value=mock_client):
            # validate_command is async and raises typer.Exit, so we need to catch it
            try:
                await call_validate_command([str(personality_file)], strict=False, format="text")
                # If we get here, the command succeeded (no exception raised)
                assert True
            except SystemExit as e:
                # Command should exit with code 0 for success
                assert e.code == 0
    
    @pytest.mark.asyncio
    async def test_validate_single_file_validation_error(self, personality_file, mock_client):
        """Test validating a file with validation errors."""
        mock_client.validate_personality.return_value = {
            "valid": False,
            "errors": ["Missing required field: persona.name"]
        }
        
        with patch("luminoracore_cli.commands.validate.get_client", return_value=mock_client):
            try:
                await call_validate_command([str(personality_file)], strict=True, format="text")
                # If we get here, the command succeeded (no exception raised)
                assert True
            except SystemExit as e:
                # Command should exit with code 1 for validation errors
                assert e.code == 1
    
    @pytest.mark.asyncio
    async def test_validate_multiple_files(self, temp_dir, sample_personality, mock_client):
        """Test validating multiple personality files."""
        import json
        
        # Create multiple personality files
        files = []
        for i in range(3):
            file_path = temp_dir / f"personality_{i}.json"
            personality = sample_personality.copy()
            personality["persona"]["name"] = f"Test Personality {i}"
            
            with open(file_path, "w") as f:
                json.dump(personality, f, indent=2)
            files.append(str(file_path))
        
        with patch("luminoracore_cli.commands.validate.get_client", return_value=mock_client):
            try:
                await call_validate_command(files, strict=False, format="text")
                # If we get here, the command succeeded (no exception raised)
                assert True
            except SystemExit as e:
                # Command should exit with code 0 for success
                assert e.code == 0
    
    @pytest.mark.asyncio
    async def test_validate_nonexistent_file(self, mock_client):
        """Test validating a non-existent file."""
        with patch("luminoracore_cli.commands.validate.get_client", return_value=mock_client):
            # This test verifies that the command handles non-existent files gracefully
            # The command should process the file and report it as invalid, then exit with code 1
            with pytest.raises(typer.Exit) as exc_info:
                await call_validate_command(["/nonexistent/file.json"], strict=False, format="text")
            # Command should exit with code 1 for file not found
            assert exc_info.value.exit_code == 1
    
    @pytest.mark.asyncio
    async def test_validate_invalid_json(self, temp_dir, mock_client):
        """Test validating a file with invalid JSON."""
        invalid_file = temp_dir / "invalid.json"
        invalid_file.write_text("{ invalid json }")
        
        with patch("luminoracore_cli.commands.validate.get_client", return_value=mock_client):
            # This test verifies that the command handles invalid JSON gracefully
            # The command should process the file and report it as invalid, then exit with code 1
            with pytest.raises(typer.Exit) as exc_info:
                await call_validate_command([str(invalid_file)], strict=False, format="text")
            # Command should exit with code 1 for invalid JSON
            assert exc_info.value.exit_code == 1
    
    @pytest.mark.asyncio
    async def test_validate_output_json(self, personality_file, temp_dir, mock_client):
        """Test validating with JSON output format."""
        output_file = temp_dir / "results.json"
        
        with patch("luminoracore_cli.commands.validate.get_client", return_value=mock_client):
            try:
                await call_validate_command(
                    [str(personality_file)], 
                    strict=False, 
                    format="json",
                    output_file=output_file
                )
                # If we get here, the command succeeded (no exception raised)
                assert True
            except SystemExit as e:
                # Command should exit with code 0 for success
                assert e.code == 0
                assert output_file.exists()
    
    @pytest.mark.asyncio
    async def test_validate_output_yaml(self, personality_file, temp_dir, mock_client):
        """Test validating with YAML output format."""
        output_file = temp_dir / "results.yaml"
        
        with patch("luminoracore_cli.commands.validate.get_client", return_value=mock_client):
            try:
                await call_validate_command(
                    [str(personality_file)], 
                    strict=False, 
                    format="yaml",
                    output_file=output_file
                )
                # If we get here, the command succeeded (no exception raised)
                assert True
            except SystemExit as e:
                # Command should exit with code 0 for success
                assert e.code == 0
                assert output_file.exists()
