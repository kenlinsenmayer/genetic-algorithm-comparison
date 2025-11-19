defmodule RunTests do
  @moduledoc """
  Test runner for Elixir One-Max GA benchmark
  """

  def main(_args \\ []) do
    OneMaxGA.run_tests(25)
  end
end

# Execute if run as script
RunTests.main(System.argv())