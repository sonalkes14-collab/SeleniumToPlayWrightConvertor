package com.example.tests;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;
import org.testng.annotations.Test;
import org.testng.annotations.BeforeMethod;
import static org.testng.Assert.assertEquals;

public class LoginTest {

    @BeforeMethod
    public void setup() {
        driver.get("https://example.com/login");
    }

    @Test
    public void testValidLogin() {
        driver.findElement(By.id("username")).sendKeys("standard_user");
        driver.findElement(By.id("password")).sendKeys("secret_sauce");
        driver.findElement(By.cssSelector(".btn_action")).click();
        
        String welcomeMessage = driver.findElement(By.className("welcome")).getText();
        assertEquals(welcomeMessage, "Welcome, user!");
    }
}
