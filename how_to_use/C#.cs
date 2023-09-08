//1- Import the txt file into your project.
//2- Change its 'Build Action' to Embedded resource and its 'Copy to Output Directory' to Copy if newer from its properties.
//3- Assign to a string array using method below;

public static string[] GetLanguageArray( )
{
return File.ReadAllText(Path.Combine(Path.GetDirectoryName(Assembly.GetExecutingAssembly().Location), @"yourPath")).Split(',');
}

// Sample location: @"Words\English.txt"
